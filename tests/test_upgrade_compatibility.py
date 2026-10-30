"""ADR0025: closed real-entry compatibility and bounded safety scenarios."""
import contextlib
import copy
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.test_cli import ROOT, CLI, load_cli_module
from tests.test_next_iteration import snapshot_tree


class UpgradeCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.source=self.root/'source'; self.project=self.root/'project'
        (self.source/'bin').mkdir(parents=True);(self.source/'.vibe/core').mkdir(parents=True)
        shutil.copy2(CLI,self.source/'bin/vibe');(self.source/'.vibe/core/version').write_text('0.13.0\n')
        (self.source/'README.md').write_text('synthetic identity B\n')
        self.project.mkdir();(self.project/'.vibe').mkdir()
        self.m=load_cli_module(); self.m.__file__=str(self.source/'bin/vibe')
        self.digest=self.m.payload_tree_sha256(self.source)
        self.config=self.project/'.vibe/upgrade-compatibility.json'
        self.declaration={'schema_version':1,'enabled':True,'rules':[{'id':'payload-admission','owner':'project-maintainer','kind':'payload-tree-allowlist','allowed_payload_tree_sha256':['a'*64]}]}
        self.write()

    def write(self): self.config.write_text(json.dumps(self.declaration))

    def args(self): return [str(self.project),'--source-ref','0.13.0','--expected-payload-tree-sha256',self.digest,'--format','json']

    def call(self, args=None, module=False):
        argv=self.args() if args is None else args
        if module:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):code=self.m.main(['check-upgrade-compatibility']+argv)
            text=out.getvalue()
        else:
            r=subprocess.run([sys.executable,'-I','-S','-B',str(self.source/'bin/vibe'),'check-upgrade-compatibility']+argv,text=True,capture_output=True,timeout=15)
            self.assertEqual(r.stderr,'');code,text=r.returncode,r.stdout
        value=json.loads(text)
        self.assertEqual(set(value),{'schema_version','command','status','compatibility','write_state','writes_performed'})
        self.assertEqual(value['write_state'],'none');self.assertIs(value['writes_performed'],False)
        data=value['compatibility']
        self.assertEqual(set(data),{'schema_version','scope','authority','source_authentication','project_binding','source','rules','findings','next_action'})
        self.assertEqual(data['source_authentication'],'not-attested')
        if data['findings']:
            self.assertEqual(len(data['findings']),1);self.assertIsNone(data['source']);self.assertEqual(data['rules'],[])
        self.assertNotIn(str(self.root),text)
        return code,value

    def finding(self, code, args=None, module=False):
        result,value=self.call(args,module)
        self.assertEqual(value['compatibility']['findings'][0]['code'],code,value)
        return value

    def test_real_cli_allowlist_unknown_no_config_and_zero_writes(self):
        baseline_declaration=copy.deepcopy(self.declaration)
        for language in ('python','node'):
            self.declaration=copy.deepcopy(baseline_declaration);self.write()
            (self.project/('pyproject.toml' if language=='python' else 'package.json')).write_text('synthetic')
            before=snapshot_tree(self.root)
            code,value=self.call();self.assertEqual(code,2)
            self.assertEqual(value['compatibility']['rules'][0]['outcome'],'adaptation-required')
            self.assertEqual(value['compatibility']['next_action']['code'],'review-maintenance-adaptation')
            self.assertEqual(snapshot_tree(self.root),before)
            self.declaration['rules'][0]['allowed_payload_tree_sha256']=['a'*64,self.digest];self.write()
            before=snapshot_tree(self.root);a=self.call();b=self.call();self.assertEqual(a,b);self.assertEqual(a[0],0)
            self.assertEqual(snapshot_tree(self.root),before)
            self.declaration['rules'].append({'id':'opaque','owner':'vibe-tech-lead','kind':'command','parameters':{'entry':'CANARY-SECRET-PATH'}});self.write()
            code,value=self.call();self.assertEqual(code,2);self.assertEqual(value['compatibility']['rules'][1]['outcome'],'not-evaluated')
            self.assertNotIn('CANARY',json.dumps(value));self.declaration['rules'].pop()
        for missing in (False,True):
            if missing:self.config.unlink()
            else:self.declaration['enabled']=False;self.write()
            before=snapshot_tree(self.root)
            with mock.patch.object(self.m,'compatibility_source_fields',side_effect=AssertionError('must not inspect source')):
                code,value=self.call([str(self.project),'--source-type','unvalidated-canary'],module=True)
            self.assertEqual((code,value['status']),(0,'not-configured'));self.assertIsNone(value['compatibility']['source'])
            self.assertEqual(snapshot_tree(self.root),before)

    def test_actual_main_never_calls_legacy_path_or_error_output(self):
        names=('source_root','framework_version','validate_source_provenance','managed_source_files','release_payload_files','dispatch_main','print_json')
        with contextlib.ExitStack() as stack:
            for name in names: stack.enter_context(mock.patch.object(self.m,name,side_effect=AssertionError('legacy path forbidden')))
            stack.enter_context(mock.patch.object(Path,'resolve',side_effect=AssertionError('resolve forbidden')))
            self.assertEqual(self.call(module=True)[1]['status'],'checked')
            self.finding('invalid-arguments',['--receipt','CANARY'],module=True)
            self.config.write_text('{bad');self.finding('invalid-declaration',module=True)
            self.config.unlink();self.assertEqual(self.call([str(self.project)],module=True)[1]['status'],'not-configured')

    def test_declaration_errors_and_fixed_paths(self):
        examples=[('{"schema_version":1,"schema_version":1}', 'invalid-declaration'), ('{"schema_version":true,"enabled":true,"rules":[]}','unsupported-schema')]
        for text,expected in examples:self.config.write_text(text);self.finding(expected)
        for mutate,expected in [
            (lambda x:x.update(extra='CANARY'),'invalid-declaration'),
            (lambda x:x['rules'].append(copy.deepcopy(x['rules'][0])),'duplicate-rule-id'),
            (lambda x:x['rules'][0].update(owner='CANARY'),'invalid-declaration'),
            (lambda x:x['rules'][0].update(kind='unknown'),'invalid-declaration'),
            (lambda x:x['rules'][0].update(allowed_payload_tree_sha256=['A'*64]),'invalid-declaration')]:
            self.declaration={'schema_version':1,'enabled':True,'rules':[{'id':'r','owner':'project-maintainer','kind':'payload-tree-allowlist','allowed_payload_tree_sha256':['a'*64]}]}
            mutate(self.declaration);self.write();value=self.finding(expected);self.assertNotIn('CANARY',json.dumps(value))

    def test_source_and_argument_failure_mapping(self):
        for args,expected in [([], 'invalid-arguments'),([str(self.project),'--format','text'],'invalid-arguments'),([str(self.project),'--source-ref','0.13.0','--source-ref','0.13.0'],'invalid-arguments'),([str(self.project)],'missing-source-evidence')]:self.finding(expected,args)
        for option,value,expected in [('--source-type','untrusted','invalid-source-type'),('--source-ref','branch-CANARY','invalid-source-ref'),('--source-ref','0.12.0','source-version-mismatch'),('--artifact-sha256','b'*64,'invalid-artifact-sha256'),('--expected-payload-tree-sha256','bad','invalid-expected-payload-sha256'),('--expected-payload-tree-sha256','b'*64,'source-digest-mismatch')]:
            args=self.args();i=args.index(option) if option in args else None
            if i is None:args += [option,value]
            else:args[i+1]=value
            self.finding(expected,args)
        for kind in ('github-release','offline-bundle'):
            self.finding('missing-source-evidence',self.args()+['--source-type',kind])
            self.assertEqual(self.call(self.args()+['--source-type',kind,'--artifact-sha256','B'*64])[1]['status'],'checked')
        url=self.args();url[url.index('--source-ref')+1]='https://github.com/mintgao/vibe-kit/releases/tag/v0.13.0'
        self.assertEqual(self.call(url)[1]['status'],'checked')
        (self.source/'.vibe/core/version').write_bytes(b'not-a-version')
        self.finding('invalid-source-version')

    def test_symlink_fifo_permission_and_resource_boundaries(self):
        self.config.unlink();os.symlink(self.source/'README.md',self.config)
        self.finding('unsafe-path');self.config.unlink();os.mkfifo(self.config)
        self.finding('unsafe-path');self.config.unlink();self.write()
        (self.source/'README.md').unlink();os.mkfifo(self.source/'README.md')
        self.finding('unsafe-path');(self.source/'README.md').unlink();(self.source/'README.md').write_text('synthetic identity B\n')
        self.config.chmod(0)
        try:self.finding('read-permission-denied')
        finally:self.config.chmod(0o600)
        self.config.write_bytes(b' '*65537);self.finding('resource-limit');self.write()
        for limit in ('entries','directories','paths','files','total','file','depth','path','component'):
            with mock.patch.dict(self.m.COMPATIBILITY_LIMITS,{limit:0}):self.finding('resource-limit',module=True)

    def test_missing_declaration_and_pinned_root_name_drift(self):
        self.config.unlink();original=self.m.CompatibilityRoot.verify
        def appear(reader):
            if reader.logical=='$.project.root':self.write()
            return original(reader)
        with mock.patch.object(self.m.CompatibilityRoot,'verify',appear):
            value=self.finding('input-changed',[str(self.project)],module=True)
            self.assertEqual(value['compatibility']['project_binding']['declaration_state'],'unavailable')
        original_read=self.m.CompatibilityRoot.read
        def replace(reader,*args,**kwargs):
            value=original_read(reader,*args,**kwargs)
            if reader.logical=='$.project.root':
                self.project.rename(self.root/'moved-project');self.project.mkdir()
            return value
        with mock.patch.object(self.m.CompatibilityRoot,'read',replace):
            value=self.finding('input-changed',module=True)
            self.assertIsNone(value['compatibility']['project_binding']['root_identity_sha256'])

    def test_second_enumeration_and_all_fixed_failure_results(self):
        original=self.m.compatibility_payload_members;calls=[]
        def limited(source,version):
            calls.append(1)
            if len(calls)==2:self.m.COMPATIBILITY_LIMITS['entries']=0
            return original(source,version)
        with mock.patch.dict(self.m.COMPATIBILITY_LIMITS,dict(self.m.COMPATIBILITY_LIMITS)):
            with mock.patch.object(self.m,'compatibility_payload_members',limited):self.finding('resource-limit',module=True)
        self.assertEqual(len(calls),2)
        for code in self.m.COMPATIBILITY_FINDINGS:
            with mock.patch.object(self.m,'compatibility_primitives',side_effect=self.m.CompatibilityFailure(code,'$')):
                exit_code,value=self.call(module=True)
            invalid=code.startswith('invalid-') or code in ('duplicate-rule-id','unsupported-schema')
            expected='invalid' if invalid else 'error' if code in ('execution-interrupted','internal-error') else 'blocked'
            self.assertEqual(value['status'],expected);self.assertEqual(exit_code,1 if invalid else 2)
            self.assertEqual(value['compatibility']['next_action'],{'code':'resolve-compatibility-input','owner':'project-maintainer'})


    def test_authenticated_plugin_direct_entry_bypasses_wrapper(self):
        plugin=self.root/'plugin';(plugin/'skills/vibe-maintain/scripts').mkdir(parents=True)
        sentinel=plugin/'skills/vibe-maintain/scripts/vibe_from_plugin.py'
        sentinel.write_text('raise AssertionError("old wrapper must never execute for preflight")\n')
        self.source.rename(plugin/'payload');self.source=plugin/'payload';self.m.__file__=str(self.source/'bin/vibe')
        self.declaration['rules'][0]['allowed_payload_tree_sha256']=[self.digest];self.write()
        before=snapshot_tree(self.root)
        code,value=self.call(self.args()+['--source-type','plugin-bundled'])
        self.assertEqual(code,0);self.assertEqual(value['compatibility']['source']['type'],'plugin-bundled')
        self.assertEqual(snapshot_tree(self.root),before)

    def test_source_ancestor_and_payload_parent_names_are_rechecked(self):
        container=self.root/'source-container';container.mkdir();self.source.rename(container/'payload');self.source=container/'payload';self.m.__file__=str(self.source/'bin/vibe')
        original=self.m.compatibility_payload_members;calls=[]
        def rename_ancestor(reader,version):
            value=original(reader,version);calls.append(1)
            if len(calls)==1:container.rename(self.root/'moved-source-container');container.mkdir()
            return value
        with mock.patch.object(self.m,'compatibility_payload_members',rename_ancestor):
            value=self.finding('input-changed',module=True)
        self.assertEqual(value['compatibility']['project_binding']['declaration_state'],'enabled')
        self.assertIsNotNone(value['compatibility']['project_binding']['root_identity_sha256'])

    def test_leaf_type_switch_is_nonblocking_and_unsafe(self):
        original=self.m.CompatibilityRoot.leaf_stat;swapped=[]
        def switch(reader,relative,*args,**kwargs):
            value=original(reader,relative,*args,**kwargs)
            if reader.logical=='$.project.root' and value is not None and not swapped:
                swapped.append(True);self.config.unlink();os.mkfifo(self.config)
            return value
        with mock.patch.object(self.m.CompatibilityRoot,'leaf_stat',switch):
            self.finding('unsafe-path',module=True)
        self.assertEqual(len(swapped),1)

    def test_source_explicit_parent_mode_drift_is_not_published(self):
        parent=self.source/'bin';parent.chmod(0o755);observations=[]
        original=self.m.compatibility_payload_members;calls=[]
        def drift(reader,version):
            value=original(reader,version);calls.append(1)
            if len(calls)==1:
                before=parent.stat();parent.chmod(0o700);after=parent.stat()
                self.assertNotEqual(stat.S_IMODE(before.st_mode),stat.S_IMODE(after.st_mode))
                observations.append({'before_mode':oct(stat.S_IMODE(before.st_mode)),'after_mode':oct(stat.S_IMODE(after.st_mode)),'before_signature':self.m.compatibility_signature(before),'after_signature':self.m.compatibility_signature(after)})
            return value
        try:
            with mock.patch.object(self.m,'compatibility_payload_members',drift):self.finding('input-changed',module=True)
        finally:
            destination=os.environ.get('VIBE_COMPATIBILITY_MODE_OBSERVATION')
            if destination:
                Path(destination).write_text(json.dumps({'observations':observations,'enumeration_calls':len(calls),'collection_outside_reader_interval':True},indent=2)+'\n')

    def test_nonfinite_opaque_parameters_rejected_without_echo(self):
        self.config.write_text('{"schema_version":1,"enabled":true,"rules":[{"id":"r","owner":"vibe-rd","kind":"command","parameters":{"number":1e999}}]}')
        self.finding('invalid-declaration')


    def test_directory_signature_finally_middle_late_and_outer_mtime(self):
        baseline_source=self.source
        for scenario in ('middle','early-failure','after-second-enumeration','outer-mtime-only'):
            with self.subTest(scenario=scenario):
                case=self.root/scenario;case.mkdir();self.source=case/'source';shutil.copytree(baseline_source,self.source)
                self.m=load_cli_module();self.m.__file__=str(self.source/'bin/vibe');self.digest=self.m.payload_tree_sha256(self.source)
                parent=self.source/('.vibe/core' if scenario=='early-failure' else '.vibe' if scenario=='middle' else 'bin')
                parent.chmod(0o755);observations=[];calls=[]
                def change():
                    first=parent.stat();parent.chmod(0o700);second=parent.stat()
                    self.assertNotEqual(stat.S_IMODE(first.st_mode),stat.S_IMODE(second.st_mode))
                    observations.append((stat.S_IMODE(first.st_mode),stat.S_IMODE(second.st_mode)))
                original_members=self.m.compatibility_payload_members;original_read=self.m.CompatibilityRoot.read
                def members(reader,version):
                    value=original_members(reader,version);calls.append(1)
                    if scenario=='middle' and len(calls)==1:change()
                    if scenario=='after-second-enumeration' and len(calls)==2:change()
                    if scenario=='outer-mtime-only' and len(calls)==1:
                        first=case.stat();os.utime(case,ns=(first.st_atime_ns,first.st_mtime_ns+1000000))
                    return value
                def read(reader,relative,*args,**kwargs):
                    value=original_read(reader,relative,*args,**kwargs)
                    if scenario=='early-failure' and reader.logical=='$.source.root' and relative=='.vibe/core/version':change()
                    return value
                if scenario=='early-failure':(self.source/'.vibe/core/version').write_text('invalid-version')
                with mock.patch.object(self.m,'compatibility_payload_members',members),mock.patch.object(self.m.CompatibilityRoot,'read',read):
                    if scenario=='outer-mtime-only':
                        code,value=self.call(module=True);self.assertEqual(value['status'],'checked');self.assertEqual(value['compatibility']['findings'],[])
                    else:
                        value=self.finding('input-changed',module=True)
                        self.assertIsNone(value['compatibility']['source']);self.assertEqual(value['compatibility']['rules'],[])
                        self.assertEqual(value['compatibility']['project_binding']['declaration_state'],'enabled')
                        self.assertIsNotNone(value['compatibility']['project_binding']['root_identity_sha256'])
                self.assertLessEqual(len(calls),2)
                if scenario!='outer-mtime-only':self.assertEqual(observations,[(0o755,0o700)])
                print('DIRECTORY-STABILITY '+json.dumps({'scenario':scenario,'observed_modes':observations,'enumerations':len(calls)}))

    def _consumed_leaf_replacement(self, declaration, kind, prior_failure=False):
        leaf=self.config if declaration else self.source/'README.md'
        original=self.m.CompatibilityRoot.verify;replaced=[]
        def verify(reader):
            if reader.logical==('$.project.root' if declaration else '$.source.root') and not replaced:
                leaf.unlink()
                if kind=='symlink':os.symlink(self.source/'.vibe/core/version',leaf)
                else:os.mkfifo(leaf)
                replaced.append(kind)
            return original(reader)
        args=self.args()
        if prior_failure:args[args.index('--expected-payload-tree-sha256')+1]='b'*64
        with mock.patch.object(self.m.CompatibilityRoot,'verify',verify):value=self.finding('input-changed',args,module=True)
        self.assertEqual(replaced,[kind]);data=value['compatibility'];self.assertIsNone(data['source']);self.assertEqual(data['rules'],[])
        self.assertIsNotNone(data['project_binding']['root_identity_sha256'])
        self.assertEqual(data['project_binding']['declaration_state'],'unavailable' if declaration else 'enabled')
        if declaration:self.assertIsNone(data['project_binding']['declaration_sha256'])
        else:self.assertEqual(data['project_binding']['declaration_sha256'],hashlib.sha256(self.config.read_bytes()).hexdigest())

    def test_consumed_declaration_final_symlink_is_changed(self):self._consumed_leaf_replacement(True,'symlink')
    def test_consumed_declaration_final_fifo_overrides_earlier_failure(self):self._consumed_leaf_replacement(True,'fifo',True)
    def test_consumed_payload_final_symlink_is_changed(self):self._consumed_leaf_replacement(False,'symlink')
    def test_consumed_payload_final_fifo_overrides_earlier_failure(self):self._consumed_leaf_replacement(False,'fifo',True)

    def test_consumed_leaf_final_permission_is_not_guessed_as_drift(self):
        original_verify=self.m.CompatibilityRoot.verify;original_stat=os.stat
        def verify(reader):
            if reader.logical!='$.project.root':return original_verify(reader)
            def denied(name,*args,**kwargs):
                if name=='upgrade-compatibility.json':raise PermissionError(errno.EACCES,'CANARY')
                return original_stat(name,*args,**kwargs)
            with mock.patch.object(os,'stat',denied):return original_verify(reader)
        with mock.patch.object(self.m.CompatibilityRoot,'verify',verify):self.finding('read-permission-denied',module=True)


    def _regression_observation(self,name,value):
        directory=os.environ.get('VIBE_COMPATIBILITY_REGRESSION_EVIDENCE')
        if directory:
            destination=Path(directory);destination.mkdir(parents=True,exist_ok=True)
            (destination/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')

    def _stream_total_growth(self, drift=False):
        maximum=self.m.COMPATIBILITY_LIMITS['total'];initial_target=maximum-16
        initial=sum(p.stat().st_size for p in self.m.release_payload_files(self.source,'0.13.0'))
        remaining=initial_target-initial;index=0
        while remaining:
            amount=min(remaining,self.m.COMPATIBILITY_LIMITS['file'])
            with (self.source/'.vibe/core'/('fill-'+str(index))).open('wb') as output:output.truncate(amount)
            remaining-=amount;index+=1
        initial=sum(p.stat().st_size for p in self.m.release_payload_files(self.source,'0.13.0'))
        self.assertEqual(initial,initial_target);self.assertLess(initial,maximum)
        self.digest=self.m.payload_tree_sha256(self.source)
        nodes={p.stat().st_ino for p in self.m.release_payload_files(self.source,'0.13.0')}
        bin_inode=(self.source/'bin/vibe').stat().st_ino;original=os.read;observed={'initial_bytes':initial,'budget':maximum,'actual_streamed_bytes':0,'growth_bytes':0}
        def read(descriptor,count):
            data=original(descriptor,count);inode=os.fstat(descriptor).st_ino
            if inode in nodes:observed['actual_streamed_bytes']+=len(data)
            if inode==bin_inode and data and not observed['growth_bytes']:
                with (self.source/'bin/vibe').open('ab') as output:output.write(b'\n'*64)
                observed['growth_bytes']=64
                if drift:(self.source/'.vibe/core/version').write_text('0.13.1\n')
            return data
        try:
            with mock.patch.object(os,'read',read):code,value=self.call(module=True)
            observed['result']=value;observed['exit_code']=code
            self.assertEqual(value['compatibility']['findings'][0]['code'],'input-changed' if drift else 'resource-limit')
            self.assertLessEqual(observed['actual_streamed_bytes'],maximum)
            self.assertEqual(observed['growth_bytes'],64)
        finally:self._regression_observation('stream-total-growth-drift' if drift else 'stream-total-growth',observed)

    def _final_verify_interrupt(self,where):
        cls=self.m.CompatibilityRoot;original_init=cls.__init__;original_verify=cls.verify;original_close=cls.close;original_stat=os.stat
        opened=[];closed=[];completed=[];closed_fds=[];injected=[];observation={'interrupted_scope':where}
        def initialize(reader,*args,**kwargs):original_init(reader,*args,**kwargs);opened.append(reader)
        def verify(reader):
            if reader.logical!=where:
                original_verify(reader);completed.append(reader.logical);return
            parent=reader.directories['.vibe/core' if where=='$.source.root' else '.vibe']
            leaf='version' if where=='$.source.root' else 'upgrade-compatibility.json'
            def interrupt(name,*args,**kwargs):
                if not injected and name==leaf and kwargs.get('dir_fd')==parent and kwargs.get('follow_symlinks') is False:
                    injected.append({'leaf':leaf,'fixed_parent_fd':parent});raise KeyboardInterrupt()
                return original_stat(name,*args,**kwargs)
            with mock.patch.object(os,'stat',interrupt):original_verify(reader)
            completed.append(reader.logical)
        def close(reader):closed.append(reader.logical);closed_fds.extend(reader.fds);original_close(reader)
        try:
            with mock.patch.object(cls,'__init__',initialize),mock.patch.object(cls,'verify',verify),mock.patch.object(cls,'close',close):code,value=self.call(module=True)
            observation['result']=value;observation['exit_code']=code
            self.assertEqual(value['compatibility']['findings'][0]['code'],'execution-interrupted')
            self.assertEqual(len(injected),1);self.assertCountEqual(closed,['$.source.root','$.project.root'])
            self.assertTrue(all(reader.fds==[] for reader in opened))
            for fd in closed_fds:
                with self.assertRaises(OSError) as caught:os.fstat(fd)
                self.assertEqual(caught.exception.errno,errno.EBADF)
            observation['all_recorded_fds_ebadf']=True
            self.assertEqual(value['compatibility']['project_binding'],{'root_identity_sha256':None,'declaration_state':'unavailable','declaration_sha256':None})
            self.assertIsNone(value['compatibility']['source']);self.assertEqual(value['compatibility']['rules'],[])
        finally:
            observation.update(closed=closed,completed=completed,injected=injected,closed_fd_count=len(closed_fds),root_states=[{'scope':reader.logical,'fds_remaining':len(reader.fds),'verification_completed':getattr(reader,'verification_completed',None),'root_verification_completed':getattr(reader,'root_verification_completed',None)} for reader in opened])
            self._regression_observation('interrupt-'+('source' if where=='$.source.root' else 'project'),observation)

    def test_source_final_verify_interrupt_closes_both_roots(self):self._final_verify_interrupt('$.source.root')
    def test_project_final_verify_interrupt_clears_unconfirmed_binding(self):self._final_verify_interrupt('$.project.root')


    def test_actual_stream_total_growth_is_bounded_at_64mib(self):self._stream_total_growth()
    def test_stream_limit_retained_when_final_drift_overrides_failure(self):self._stream_total_growth(True)

    def test_single_file_growth_still_refused_with_total_room(self):
        leaf=self.source/'README.md';maximum=self.m.COMPATIBILITY_LIMITS['file']
        with leaf.open('wb') as output:output.truncate(maximum-16)
        self.digest=self.m.payload_tree_sha256(self.source);inode=leaf.stat().st_ino;original=os.read;observed={'bytes':0,'grown':False}
        def read(fd,count):
            data=original(fd,count)
            if os.fstat(fd).st_ino==inode:
                observed['bytes']+=len(data)
                if data and not observed['grown']:
                    with leaf.open('ab') as output:output.write(b'x'*32)
                    observed['grown']=True
            return data
        with mock.patch.object(os,'read',read):self.finding('resource-limit',module=True)
        self.assertLessEqual(observed['bytes'],maximum);self.assertTrue(observed['grown'])
        self._regression_observation('single-file-control',observed)
