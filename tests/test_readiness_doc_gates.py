"""Behavioral evidence for ADR0014; no host-authentication claims."""
import copy
import io
import contextlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

from tests.test_cli import ROOT, CLI, run_cli, load_cli_module, profile_test_intent, profile_test_receipt, passing_command


class ReadinessDocGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.m = load_cli_module()
        self.brief = 'docs/work-items/test/brief.md'
        self.path = self.root / self.brief
        self.path.parent.mkdir(parents=True)
        self.original = (ROOT / 'docs/work-items/20260908-readiness-doc-gates-release/brief.md').read_text()
        self.original = self.original.replace('docs/decisions/0014-readiness-doc-gates-v09-publication.md', 'docs/decisions/0001-test.md').replace('docs/work-items/20260908-readiness-doc-gates-release/technical-review.md#Pass 2 — approved', 'review.md#approved')
        self.path.write_text(self.original)
        self.adr = self.root / 'docs/decisions/0001-test.md'
        self.adr.parent.mkdir(parents=True)
        self.adr.write_text('# 0001: Test\n\n- Status: Accepted\n\n## Decision\n\nBounded test.\n')
        (self.root / 'review.md').write_text('# Approved review\n')

    def findings(self, text=None):
        if text is not None:
            self.path.write_text(text)
        return self.m.readiness_findings(self.root, self.brief)

    def test_accepted_adr_and_real_cli_read_only(self):
        self.assertEqual(self.findings(), [])
        before = self.path.read_bytes()
        result = run_cli(CLI, 'validate-readiness', str(self.root), '--brief', self.brief, '--format', 'json')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)['writes_performed'])
        self.assertEqual(self.path.read_bytes(), before)

    def test_implemented_missing_wrong_kind_and_spoofed_adrs_fail(self):
        for body in ['# 0001: Test\n- Status: implemented\n', '# 0001: Test\n```md\n- Status: Accepted\n```\n', '# 0001: Test\n- Status: Accepted\n- Status: Rejected\n', '# 0099: Wrong\n- Status: Accepted\n']:
            with self.subTest(body=body):
                self.adr.write_text(body)
                self.assertTrue(self.findings())
        self.adr.unlink()
        self.assertTrue(self.findings())
        note = self.root / 'implemented.md'
        note.write_text('# Note\n- Status: Accepted\n')
        self.assertTrue(self.findings(self.original.replace('docs/decisions/0001-test.md', 'implemented.md')))

    def test_missing_duplicate_unknown_fenced_and_continued_fields_fail(self):
        for old,new in [('- Gate: `implementation-ready`',''),('- Gate: `implementation-ready`','- Gate: `implementation-ready`\n- Gate: blocked'),('- Size: `L`','- Size: `S`'),('- Size: `L`','- Size: `M`\n- Size: `L`'),('- Outcome: `decision-accepted`','- Outcome: unknown'),('- Open blockers: none','- Open blockers: unresolved'),('- Confirmed at:', '- Bad time:'),('## Technical decision readiness','```md\n## Technical decision readiness'),('- Decision owner:', '  continued prose\n- Decision owner:')]:
            with self.subTest(old=old,new=new):
                self.assertTrue(self.findings(self.original.replace(old,new)))

    def test_paths_escape_symlink_and_missing_review_fail(self):
        for path in ['../outside.md','/tmp/outside.md','docs/decisions/../0001-test.md']:
            self.assertTrue(self.findings(self.original.replace('docs/decisions/0001-test.md',path)))
        self.path.write_text(self.original)
        self.adr.unlink()
        self.adr.symlink_to(self.root/'review.md')
        self.assertTrue(self.findings())
        self.adr.unlink()
        self.adr.write_text('# 0001: Test\n- Status: Accepted\n')
        (self.root/'review.md').unlink()
        self.assertTrue(self.findings())

    def test_no_new_decision_M_L_and_invalid_review_or_rationale(self):
        text=self.original.replace('`decision-accepted`','`no-new-durable-decision`').replace('`docs/decisions/0001-test.md`','none').replace('- No-new-decision rationale: none','- No-new-decision rationale: Local reversible implementation under existing boundaries.')
        self.assertEqual(self.findings(text),[])
        m=text.replace('- Size: `L`','- Size: `M`')
        trigger=next(line for line in m.splitlines() if line.startswith('- Trigger evidence:'))
        m=m.replace(trigger,'- Trigger evidence: none').replace('- Review mode: `independent-agent`','- Review mode: `not-required`').replace('- Review result: `approved`','- Review result: `not-required`').replace('- Review evidence: `review.md#approved`','- Review evidence: none')
        self.assertEqual(self.findings(m),[])
        for bad in [text.replace('- Review result: `approved`','- Review result: `pending`'),text.replace('Local reversible implementation under existing boundaries.','none'),m.replace('`no-new-durable-decision`','`covered-by-accepted-decision`'),text.replace('- Gate: `implementation-ready`','- Gate: `blocked`')]:
            self.assertTrue(self.findings(bad))

    def agents(self, block=None):
        block=block or self.m.AGENTS_START+'\n'+('managed '*903)+self.m.AGENTS_END
        # The exact documented report shape, with markers included in 909 managed words.
        block=self.m.AGENTS_START+'\n'+('managed '*(909-len((self.m.AGENTS_START+' '+self.m.AGENTS_END).split())))+self.m.AGENTS_END
        raw='前缀 '+block+'\n'+('project '*1948)
        (self.root/'AGENTS.md').write_text(raw)
        (self.root/'.vibe').mkdir(exist_ok=True)
        (self.root/'.vibe/manifest.json').write_text(json.dumps({'schema_version':1,'framework_version':'0.9.0','managed_files':{},'agents_block_hash':self.m.sha256_text(block)}))
        return raw,block

    def test_authenticated_span_whole_file_2858_exceeds_2800(self):
        raw,block=self.agents()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code=self.m.inspect_managed_agents(self.root,'unicode-whitespace-v1',2800,'json')
        result=json.loads(output.getvalue())
        self.assertEqual(code,1)
        self.assertEqual(result['word_check']['actual'],2858)
        self.assertEqual(result['word_check']['managed_words'],909)
        self.assertEqual(raw.encode()[result['byte_span']['start']:result['byte_span']['end']],block.encode())
        self.assertEqual((self.root/'AGENTS.md').read_text(),raw)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.m.inspect_managed_agents(self.root,'unicode-whitespace-v1',2858,'json'),0)
        result=run_cli(CLI,'inspect-managed-agents',str(self.root),'--word-policy','unknown','--max-words','2858','--format','json')
        self.assertNotEqual(result.returncode,0)

    def test_agents_tampering_duplicate_reversed_markers_and_invalid_manifest(self):
        raw,block=self.agents()
        for bad in [raw.replace('managed','changed',1),raw+self.m.AGENTS_START,self.m.AGENTS_END+self.m.AGENTS_START]:
            (self.root/'AGENTS.md').write_text(bad)
            with self.assertRaises(self.m.VibeError):
                self.m.inspect_managed_agents(self.root,None,None,'json')
        (self.root/'AGENTS.md').write_text(raw)
        (self.root/'.vibe/manifest.json').write_text('{}')
        with self.assertRaises(self.m.VibeError):self.m.inspect_managed_agents(self.root,None,None,'json')

    def test_v09_profile_cross_identity_and_authorization_rejections(self):
        intent=profile_test_intent(self.m,3)
        self.assertEqual(self.m.validate_publication_intent(intent),[])
        self.assertTrue(self.m.validate_v080_intent(intent))
        for key,value in [('schema_version',2),('version','0.8.0'),('profile','unknown'),('issue_closeout_policy',{'mode':'none','issues':[],'allowed_operations':[]})]:
            bad=copy.deepcopy(intent);bad[key]=value
            self.assertTrue(self.m.validate_publication_intent(bad))
        duplicate=copy.deepcopy(intent)
        duplicate['assets'][1]=copy.deepcopy(duplicate['assets'][0])
        duplicate['asset_set_sha256']=self.m.canonical_json_sha256(duplicate['assets'])
        self.assertTrue(self.m.validate_publication_intent(duplicate))
        auth={'authorization_id':'approved-existing','repository':'mintgao/vibe-kit','version':'0.9.0','release_kind':'prerelease','allowed_operations':list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS),'publication_intent_sha256':self.m.canonical_json_sha256(intent),'host_operation_id':'host-1','authorization_source_ref':'task:user-request','bound_at':'2026-09-08T00:00:00Z'}
        self.assertEqual(self.m.validate_profile_authorization(auth,intent,profile=self.m.PUBLICATION_PROFILES[3]),[])
        for key in ('bound_at','authorization_source_ref','publication_intent_sha256'):
            bad=dict(auth);bad[key]=''
            self.assertTrue(self.m.validate_profile_authorization(bad,intent,profile=self.m.PUBLICATION_PROFILES[3]))
        with self.assertRaises(self.m.VibeError):self.m.build_v090_closeout_intent({},intent,{},auth,{}, {})

    def test_v09_phase_mapping_is_closed(self):
        profile=self.m.PUBLICATION_PROFILES[3];commit='1'*40;tree='2'*40
        value={'schema_version':1,'kind':profile['kinds']['prepublication-qa'],'execution_id':'qa','executor_role':'independent-qa','started_at':'2026-09-08T00:00:00Z','finished_at':'2026-09-08T00:01:00Z','repository':'mintgao/vibe-kit','version':'0.9.0','profile':profile['profile'],'source_commit':commit,'source_tree_oid':tree,'asset_set_sha256':None,'commands':[passing_command(0,'test')],'criterion_mapping':[{'criterion_id':key,'state':state,'evidence_command_sequences':[] if state=='not-runnable-before-publication' else [0],'postpublication_requirement':profile['requirements'][key]} for key,state in profile['states'].items()],'status':'passed','error':None}
        self.assertEqual(self.m.validate_profile_qa_receipt(value,commit,tree,profile=profile),[])
        value['criterion_mapping'][-1]['state']='passed'
        self.assertTrue(self.m.validate_profile_qa_receipt(value,commit,tree,profile=profile))

    def test_healthy_v08_upgrade_preserves_project_owned_bytes(self):
        archive=subprocess.run(['git','archive','--format=tar','v0.8.0'],cwd=ROOT,check=True,capture_output=True).stdout
        predecessor=self.root/'predecessor';predecessor.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive),mode='r:') as bundle:bundle.extractall(predecessor)
        target=self.root/'target'
        result=run_cli(predecessor/'bin/vibe','init',str(target))
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        owned='\n<!-- owner -->\nProject policy stays: café 中文.\n'
        with (target/'AGENTS.md').open('a') as stream:stream.write(owned)
        result=run_cli(target/'bin/vibe','doctor',str(target),'--format','json')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        result=run_cli(CLI,'upgrade',str(target),'--format','json','--source-type','local-payload','--source-ref','0.9.0')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue((target/'AGENTS.md').read_text().endswith(owned))
        result=run_cli(target/'bin/vibe','doctor',str(target),'--format','json')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_managed_paragraphs_and_bilingual_release_review_contract(self):
        block=self.m.extract_agents_block((ROOT/'AGENTS.md').read_text())
        for para in block.replace(self.m.AGENTS_START, '').replace(self.m.AGENTS_END, '').strip().split('\n\n'):
            if para and not para.startswith(('#','-','1.','<!--')):
                self.assertNotIn('\n',para)
        for filename in ['README.md','README.zh-CN.md']:
            text=(ROOT/filename).read_text()
            for fact in ('v0.9.0','validate-readiness','inspect-managed-agents','unicode-whitespace-v1','2858','2800'):
                self.assertIn(fact,text)
        release=(ROOT/'.agents/skills/vibe-release/SKILL.md').read_text()
        for fact in ('README.md','README.zh-CN.md','unchanged','Before final'):
            self.assertIn(fact,release)


    def test_v09_receipt_exact_seven_smokes_and_profile_binding(self):
        intent=profile_test_intent(self.m,3)
        receipt=profile_test_receipt(self.m,intent,3)
        self.assertEqual(self.m.validate_publication_receipt_shape(receipt,intent),[])
        for mutate in [lambda r:r['smokes'].pop(),lambda r:r['downloads'].pop(),lambda r:r.update(schema_version=2),lambda r:r['operations'][3]['asset_receipts'].pop(),lambda r:r.update(issue_closeout={})]:
            bad=copy.deepcopy(receipt);mutate(bad)
            self.assertTrue(self.m.validate_publication_receipt_shape(bad,intent))

    def test_closeout_exact_scope_monotonic_resume_and_standalone_receipt(self):
        digest='a'*64
        identifier=self.m.profile_closeout_id(digest,version='0.9.0',schema=2,issues=[6,7])
        issues=[];snapshots=[];operations=[]
        for index,number in enumerate([6,7]):
            body=f'Problem fixed; regression test; public v0.9.0. <!-- vibe-kit:v0.9.0:issue-{number}:{identifier} -->'
            issues.append({'issue_number':number,'comment_body':body,'observed_state':'open','observed_matching_comment_id':None,'criterion_evidence_sha256':'b'*64})
            snapshot={'issue_number':number,'state':'open','marker_state':'absent','matching_comment_id':None,'matching_comment_body_sha256':None}
            snapshots.append(snapshot)
            for offset,kind in enumerate(['create-exact-evidence-comment','close-issue']):
                comment=offset==0
                operations.append({'sequence':2*index+offset,'operation_id':f"issue-{number}-{'comment' if comment else 'close'}",'issue_number':number,'kind':kind,'natural_key':f'issue:{number}:marker:{identifier}' if comment else f'issue:{number}:state:closed','expected_precondition':{'kind':'issue-closeout-monotonic-resume','initial_snapshot_sha256':self.m.canonical_json_sha256(snapshot),'allowed_observations':['open-absent','open-exact','closed-exact'] if comment else ['open-exact','closed-exact']},'max_write_attempts':2})
        request={'parent_publication_intent_sha256':digest,'publication_receipt_sha256':'c'*64,'verification_receipt_sha256':'d'*64,'repository':self.m.publication_repository(),'issues':issues,'remote_snapshot':{'observed_at':'2026-09-08T00:00:00Z','issues':snapshots},'operations':operations,'authorization_scope':{'repository':'mintgao/vibe-kit','issues':[6,7],'allowed_operations':['create-exact-evidence-comment','close-issue'],'destructive_operations_allowed':False,'requires_separate_closeout_authorization':True}}
        intent,bodies=self.m.build_profile_closeout_intent(request,version='0.9.0',schema=2,issue_numbers=[6,7],parent_digest=digest)
        self.assertEqual(intent['schema_version'],2)
        self.assertEqual(len(bodies),2)
        with self.assertRaises(self.m.VibeError):self.m.build_closeout_intent(request)
        for mutate in [lambda r:r['issues'].reverse(),lambda r:r['operations'].reverse(),lambda r:r['remote_snapshot']['issues'][0].update(state='closed'),lambda r:r['remote_snapshot']['issues'][0].update(marker_state='duplicate')]:
            bad=copy.deepcopy(request);mutate(bad)
            with self.assertRaises(self.m.VibeError):self.m.build_profile_closeout_intent(bad,version='0.9.0',schema=2,issue_numbers=[6,7],parent_digest=digest)
        auth={'closeout_authorization_id':'close-auth','repository':'mintgao/vibe-kit','issues':[6,7],'allowed_operations':['create-exact-evidence-comment','close-issue'],'closeout_intent_sha256':self.m.canonical_json_sha256(intent),'destructive_operations_allowed':False,'authorization_source_ref':'task:existing-user-request','bound_at':'2026-09-08T00:00:00Z'}
        receipt={'schema_version':2,'kind':'vibe-kit-issue-closeout-receipt','closeout_id':identifier,'closeout_intent_sha256':self.m.canonical_json_sha256(intent),'closeout_authorization_id':'close-auth','overall_state':'confirmed-complete','items':[{'issue_number':n,'expected_initial_state':'open','comment_body_sha256':intent['issues'][i]['comment_body_sha256'],'comment_id':100+n,'comment_url':f'https://github.com/mintgao/vibe-kit/issues/{n}#issuecomment-{100+n}','comment_write_state':'created','close_write_state':'read-matched','observed_post_state':'closed','read_back':True,'error':None} for i,n in enumerate([6,7])]}
        self.assertEqual(self.m.validate_v090_closeout_receipt(receipt,intent,auth),[])
        for mutate in [lambda r:r['items'].reverse(),lambda r:r['items'][0].update(read_back=False),lambda r:r['items'][0].update(comment_url='https://example.invalid'),lambda r:r.update(schema_version=1),lambda r:r['items'][0].update(close_write_state='updated')]:
            bad=copy.deepcopy(receipt);mutate(bad)
            self.assertTrue(self.m.validate_v090_closeout_receipt(bad,intent,auth))

    def test_postpublication_parent_requires_same_verified_profile_and_authorization(self):
        profile=self.m.PUBLICATION_PROFILES[3]
        intent=profile_test_intent(self.m,3);receipt=profile_test_receipt(self.m,intent,3)
        digest=self.m.canonical_json_sha256
        auth={'authorization_id':receipt['authorization_id'],'repository':'mintgao/vibe-kit','version':'0.9.0','release_kind':'prerelease','allowed_operations':list(self.m.V080_PUBLICATION_ALLOWED_OPERATIONS),'publication_intent_sha256':digest(intent),'host_operation_id':receipt['host_operation_id'],'authorization_source_ref':'task:accepted','bound_at':'2026-09-08T00:00:00Z'}
        validation={'command':'validate-publication','status':'valid','profile':profile['profile'],'intent_sha256':digest(intent),'authorization_id':auth['authorization_id'],'host_operation_id':auth['host_operation_id']}
        acceptance={'schema_version':1,'kind':profile['kinds']['postpublication-acceptance'],'execution_id':'post-qa','executor_role':'independent-qa','started_at':'2026-09-08T00:00:00Z','finished_at':'2026-09-08T00:01:00Z','repository':'mintgao/vibe-kit','version':'0.9.0','profile':profile['profile'],'source_commit':intent['source_commit'],'source_tree_oid':'e'*40,'publication_intent_sha256':digest(intent),'authorization_id':auth['authorization_id'],'host_operation_id':auth['host_operation_id'],'validate_publication_result_sha256':digest(validation),'criteria':[{'criterion_id':key,'state':'passed','evidence_refs':[{'kind':'publication-receipt','sha256':digest(receipt)}]} for key in profile['post_criteria']],'status':'passed','error':None}
        self.assertEqual(self.m.validate_v090_closeout_parent(intent,receipt,auth,acceptance,validation),[])
        for key,value in [('schema_version',2),('verification_state','not-run'),('authorization_id','different')]:
            bad=copy.deepcopy(receipt);bad[key]=value
            self.assertTrue(self.m.validate_v090_closeout_parent(intent,bad,auth,acceptance,validation))
        bad=copy.deepcopy(acceptance);bad['criteria'].append({'criterion_id':'AC-CLOSE.1','state':'passed','evidence_refs':[]})
        self.assertTrue(self.m.validate_v090_closeout_parent(intent,receipt,auth,bad,validation))


    def test_readiness_literals_require_plain_or_exactly_one_paired_backtick(self):
        for size in ('M', 'L', '`M`', '`L`'):
            with self.subTest(size=size):
                self.assertEqual(self.findings(self.original.replace('- Size: `L`', '- Size: ' + size)), [])
        for size in ('`L', 'L`', '``L``', '``L`', '`L``', '` M`', '`L `', 'M L'):
            with self.subTest(size=size):
                findings = self.findings(self.original.replace('- Size: `L`', '- Size: ' + size))
                self.assertTrue(any(item['rule'] == 'readiness.size' for item in findings))
        for field, value in (('Outcome', 'decision-accepted'), ('Gate', 'implementation-ready'), ('Review mode', 'independent-agent'), ('Review result', 'approved')):
            for malformed in ('`' + value, value + '`', '``' + value + '``'):
                with self.subTest(field=field, malformed=malformed):
                    findings = self.findings(self.original.replace(f'- {field}: `{value}`', f'- {field}: {malformed}'))
                    self.assertTrue(any(item['rule'] == 'readiness.enum' and item['location'] == field for item in findings))
