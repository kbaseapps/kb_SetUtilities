# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import re
import sys
import uuid
from datetime import datetime
from pprint import pformat  # ,pprint

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.SetAPIServiceClient import SetAPI
from installed_clients.WorkspaceClient import Workspace as workspaceService
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.kb_MsuiteClient import kb_Msuite
from installed_clients.kb_hmmerClient import kb_hmmer
#END_HEADER


class kb_SetUtilities:
    '''
    Module Name:
    kb_SetUtilities

    Module Description:
    ** A KBase module: kb_SetUtilities
**
** This module contains basic utilities for set manipulation, originally extracted
** from kb_util_dylan
**
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "1.8.0"
    GIT_URL = "https://github.com/kbaseapps/kb_SetUtilities"
    GIT_COMMIT_HASH = "b1763a92e7786b049ba38a6f2d49667c08fd7025"

    #BEGIN_CLASS_HEADER
    workspaceURL = None
    shockURL = None
    handleURL = None
    serviceWizardsURL = None
    callbackURL = None
    scratch = None

    def now_ISO(self):
        now_timestamp = datetime.now()
        now_secs_from_epoch = (now_timestamp - datetime(1970,1,1)).total_seconds()
        now_timestamp_in_iso = datetime.fromtimestamp(int(now_secs_from_epoch)).strftime('%Y-%m-%d_%T')
        return now_timestamp_in_iso

    def log(self, target, message):
        # target is a list for collecting log messages
        message = '['+self.now_ISO()+'] '+message
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()

    def check_params (self, params, required_params):
        missing_params = []
        for param in required_params:
            if not params.get(param):
                missing_params.append(param)
        if len(missing_params):
            raise ValueError("Missing required param(s):\n" + "\n".join(missing_params))

    def ws_fetch_error(self, obj_desc, obj_ref, error=None):
        msg = 'Unable to fetch '+obj_desc+' ref:'+ obj_ref + ' from workspace.'
        if error is not None:
            msg += ' Error: ' + str(error)
        raise ValueError(msg)

    def set_provenance (self, ctx, input_ws_obj_refs=[], service_name=None, method_name=None):
        if ctx.get('provenance '):
            provenance = ctx['provenance']
        else:
            provenance = [{}]
        # add additional info to provenance here, especially the input data object reference(s)
        if 'input_ws_objects' not in provenance[0]:
            provenance[0]['input_ws_objects'] = []
        if len(input_ws_obj_refs) > 0:
            provenance[0]['input_ws_objects'].extend(input_ws_obj_refs)
        if service_name is not None:
            provenance[0]['service'] = service_name
        if method_name is not None:
            provenance[0]['method'] = method_name
        return provenance

    def get_obj_name_and_type_from_obj_info (self, obj_info, full_type=False):
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        obj_name = obj_info[NAME_I]
        obj_type = obj_info[TYPE_I].split('-')[0]
        if not full_type:
            obj_type = obj_type.split('.')[1]
        return (obj_name, obj_type)

    def get_obj_ref_from_obj_info (self, obj_info):
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        return '/'.join([str(obj_info[WSID_I]),
                         str(obj_info[OBJID_I]),
                         str(obj_info[VERSION_I])])
        
    def get_obj_ref_from_obj_info_noVer (self, obj_info):
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        return '/'.join([str(obj_info[WSID_I]),
                         str(obj_info[OBJID_I])])
        
    def get_obj_data (self, obj_ref, obj_type_desc, full_type=False):
        obj_data = None
        obj_info = None
        obj_name = None
        obj_type = None
        try:
            objects = self.wsClient.get_objects2({'objects': [{'ref': obj_ref}]})['data'][0]
        except Exception as e:
            self.ws_fetch_error(obj_type_desc+' object', obj_ref, error=e)
        obj_data = objects['data']
        obj_info = objects['info']
        (obj_name, obj_type) = self.get_obj_name_and_type_from_obj_info (obj_info, full_type)
        return (obj_data, obj_info, obj_name, obj_type)

    def get_obj_info (self, obj_ref, obj_type_desc, full_type=False):
        obj_info = None
        obj_name = None
        obj_type = None
        try:
            obj_info = self.wsClient.get_object_info_new ({'objects':[{'ref':obj_ref}]})[0]
        except Exception as e:
            self.ws_fetch_error(obj_type_desc+' object info', obj_ref, error=e)
        (obj_name, obj_type) = self.get_obj_name_and_type_from_obj_info (obj_info, full_type)
        return (obj_info, obj_name, obj_type)
    
    def get_newest_obj_info (self, old_obj_ref, obj_type_desc, full_type=False):
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        obj_info = None
        obj_name = None
        obj_type = None
        try:
            obj_info = self.wsClient.get_object_info_new ({'objects':[{'ref':old_obj_ref}]})[0]
        except Exception as e:
            self.ws_fetch_error(obj_type_desc+' object info', old_obj_ref, error=e)
        (obj_name, obj_type) = self.get_obj_name_and_type_from_obj_info (obj_info, full_type)

        # get newest ref
        wsid = obj_info[WSID_I]
        try:
            newest_obj_info = self.wsClient.get_object_info_new ({'objects':[{'wsid':wsid,'name':obj_name}]})[0]
        except Exception as e:
            self.ws_fetch_error(obj_type_desc+' object info', obj_name, error=e)
        return (newest_obj_info, obj_name, obj_type)
    
    def get_obj_info_list_from_ws_id (self, ws_id, obj_type, obj_type_desc):
        obj_info_list = []
        try:
            obj_info_list = self.wsClient.list_objects({'ids':[ws_id],'type':obj_type})
        except Exception as e:
            raise ValueError ("Unable to list "+obj_type_desc+" objects from workspace: "+str(ws_id)+" "+str(e))
        return obj_info_list

    def get_obj_info_list_from_ws_name (self, ws_name, obj_type, obj_type_desc):
        obj_info_list = []
        try:
            obj_info_list = self.wsClient.list_objects({'workspaces':[ws_name],'type':obj_type})
        except Exception as e:
            raise ValueError ("Unable to list "+obj_type_desc+" objects from workspace: "+str(ws_id)+" "+str(e))
        return obj_info_list

    def get_genome_attribute (self, genome_data, attr, genome_tag=None):
        val = None
        known_attrs = ['sci_name',
                       'taxonomy',
                       'contig_count',
                       'genome_length',
                       'N50',
                       'GC',
                       'CDS_count',
                       'tRNA_count',
                       '5S_rRNA_count',
                       '16S_rRNA_count',
                       '23S_rRNA_count',
                       'CRISPR_array_count']
        if attr not in known_attrs:
            raise ValueError ("Uknown attr '"+attr+"' requested in get_genome_attribute(")

        # handy functions
        def _get_genome_id (genome_data, genome_tag):
            genome_id = ''
            if genome_tag is not None:
                genome_id = genome_tag
            elif genome_data.get('id'):
                genome_id = genome_data['id']
            return genome_id
            
        def _check_feature_func (f, target_str_list):
            hit = False
            if f.get('function'):
                func = f['function']
                for target in target_str_list:
                    if func.startswith(target):
                        hit = True
            if len(f.get('functions',[])) > 0:
                for func in f['functions']:
                    for target in target_str_list:
                        if func.startswith(target):
                            hit = True
                            break
            if hit:
                return 1
            return 0

        # sci_name
        if attr == 'sci_name':
            val = '-'
            if genome_data.get('scientific_name'):
                val = genome_data['scientific_name']

        # taxonomy
        elif attr == 'taxonomy':
            val = '-'
            if genome_data.get('taxonomy'):
                val = genome_data['taxonomy']

        # contig_count
        elif attr == 'contig_count':
            if genome_data.get('num_contigs',0) > 0:
                val = genome_data['num_contigs']
            elif len(genome_data.get('contig_ids',[])) > 0:
                val = len(genome_data['contig_ids'])
            elif len(genome_data.get('contig_lengths',[])) > 0:
                val = len(genome_data['contig_lengths'])
            elif genome_data.get('assembly_ref'):
                (assembly_obj_data,
                 assembly_obj_info,
                 assembly_obj_name,
                 assembly_obj_type) = self.get_obj_data(genome_data['assembly_ref'], 'assembly')
                if assembly_obj_data.get('num_contigs',0) > 0:
                    val = assembly_obj_data['num_contigs']
                elif len(assembly_obj_data.get('contigs',{}).keys()) > 0:
                    val = len(assembly_obj_data['contigs'].keys())
                else:
                    genome_id = _get_genome_id (genome_data, genome_tag)
                    raise ValueError ("assembly for genome "+genome_id+" missing all necessary fields for "+attr)
            else:
                genome_id = _get_genome_id (genome_data, genome_tag)
                raise ValueError ("genome "+genome_id+" missing all necessary fields for "+attr)

        # genome_length
        elif attr == 'genome_length':
            if genome_data.get('dna_size',0) > 0:
                val = genome_data['dna_size']
            elif len(genome_data.get('contig_lengths',[])) > 0:
                val = 0
                for contig_len in genome_data.get('contig_lengths'):
                    val += contig_len
            elif genome_data.get('assembly_ref'):
                (assembly_obj_data,
                 assembly_obj_info,
                 assembly_obj_name,
                 assembly_obj_type) = self.get_obj_data(genome_data['assembly_ref'], 'assembly')
                if assembly_obj_data.get('dna_size',0) > 0:
                    val = assembly_obj_data['dna_size']
                elif len(assembly_obj_data.get('contigs',{}).keys()) > 0:
                    val = 0
                    for contig_id in assembly_obj_data['contigs'].keys():
                        if assembly_obj_data['contigs'][contig_id].get('length',0) > 0:
                            val += assembly_obj_data['contigs'][contig_id].get('length')
                else:
                    genome_id = _get_genome_id (genome_data, genome_tag)
                    raise ValueError ("assembly for genome "+genome_id+" missing all necessary fields for "+attr)
            else:
                genome_id = _get_genome_id (genome_data, genome_tag)
                raise ValueError ("genome "+genome_id+" missing all necessary fields for "+attr)

        # N50
        elif attr == 'N50':
            total_length = self.get_genome_attribute (genome_data, 'genome_length', genome_tag)
            half_length = int((0.5*float(total_length)+0.5))
            sorted_contig_lengths = []
            
            if len(genome_data.get('contig_lengths',[])) > 0:
                sorted_contig_lengths = sorted(genome_data['contig_lengths'], key=int, reverse=True)
            elif genome_data.get('assembly_ref'):
                (assembly_obj_data,
                 assembly_obj_info,
                 assembly_obj_name,
                 assembly_obj_type) = self.get_obj_data(genome_data['assembly_ref'], 'assembly')
                if len(assembly_obj_data.get('contigs',{}).keys()) > 0:
                    contig_lengths = []
                    for contig_id in assembly_obj_data['contigs'].keys():
                        if assembly_obj_data['contigs'][contig_id].get('length',0) > 0:
                            contig_lengths.append(assembly_obj_data['contigs'][contig_id].get('length'))
                else:
                    genome_id = _get_genome_id (genome_data, genome_tag)
                    raise ValueError ("assembly for genome "+genome_id+" missing all necessary fields for "+attr)
                sorted_contig_lengths = sorted(contig_lengths, key=int, reverse=True)
            else:
                genome_id = _get_genome_id (genome_data, genome_tag)
                raise ValueError ("genome "+genome_id+" missing all necessary fields for "+attr)

            running_sum = 0
            N50 = 0
            for contig_length in sorted_contig_lengths:
                running_sum += contig_length
                if running_sum >= half_length:
                    N50 = contig_length
            val = N50
        
        # GC
        elif attr == 'GC':
            GC = '-'
            if genome_data.get('gc_content'):
                GC = str(round(100*genome_data['gc_content'],2))+'%'
            elif genome_data.get('assembly_ref'):
                (assembly_obj_data,
                 assembly_obj_info,
                 assembly_obj_name,
                 assembly_obj_type) = self.get_obj_data(genome_data['assembly_ref'], 'assembly')
                GC = '-'
                if assembly_obj_data.get('gc_content'):
                    GC = str(round(100*assembly_obj_data['gc_content'],2))+'%'
                elif len(assembly_obj_data.get('contigs',{}).keys()) > 0:
                    total_length = self.get_genome_attribute (genome_data, 'genome_length', genome_tag)
                    running_weighted_sum = 0
                    for contig_id in assembly_obj_data['contigs'].keys():
                        if assembly_obj_data['contigs'][contig_id].get('length',0) > 0 and \
                           assembly_obj_data['contigs'][contig_id].get('gc_content',0) > 0:
                            this_length = assembly_obj_data['contigs'][contig_id]['length']
                            this_gc = assembly_obj_data['contigs'][contig_id]['gc_content']
                            running_weighted_sum += this_length * this_gc
                    GC = str(round(100*(float(running_weighted_sum)/float(total_length)),2))+'%'
                if str(GC) == '-':
                    if assembly_obj_data.get('base_counts'):
                        base_counts = assembly_obj_data['base_counts']
                        total_bases = base_counts['A'] + base_counts['T'] + base_counts['G'] + base_counts['C']
                        gc_content = float(base_counts['G'] + base_counts['C']) / float(total_bases)
                        GC = str(round(100*gc_content,2))+'%'
                        
                if str(GC) == '-':
                    genome_id = _get_genome_id (genome_data, genome_tag)
                    raise ValueError ("assembly for genome "+genome_id+" missing all necessary fields for "+attr)
                sorted_contig_lengths = sorted(contig_lengths, key=int, reverse=True)
            else:
                genome_id = _get_genome_id (genome_data, genome_tag)
                raise ValueError ("genome "+genome_id+" missing all necessary fields for "+attr)
            val = GC
            
        # CDS count
        elif attr == 'CDS_count':
            val = '-'
            if len(genome_data.get('cdss',[])) > 0:
                val = len(genome_data['cdss'])

        # tRNA_count
        elif attr == 'tRNA_count':
            val = 0
            #tRNAs_seen = dict()  # function string doesn't always include anti-codon
            if 'non_coding_features' in genome_data:
                for f in genome_data['non_coding_features']:
                    val += _check_feature_func (f, ['tRNA'])
                #val += len(tRNAs_seen.keys())

        # 5S_rRNA_count
        elif attr == '5S_rRNA_count':
            val = 0
            if 'non_coding_features' in genome_data:
                for f in genome_data['non_coding_features']:
                    val += _check_feature_func (f, ['5S rRNA',
                                                    '5S ribosomal RNA'])

        # 16S_rRNA_count
        elif attr == '16S_rRNA_count':
            val = 0
            if 'non_coding_features' in genome_data:
                for f in genome_data['non_coding_features']:
                    val += _check_feature_func (f, ['16S rRNA',
                                                    '16S ribosomal RNA',
                                                    'SSU rRNA',
                                                    'SSU ribosomal RNA'])

        # 23S_rRNA_count
        elif attr == '23S_rRNA_count':
            val = 0
            if 'non_coding_features' in genome_data:
                for f in genome_data['non_coding_features']:
                    val += _check_feature_func (f, ['23S rRNA',
                                                    '23S ribosomal RNA',
                                                    'LSU rRNA',
                                                    'LSU ribosomal RNA'])

        # CRISPR_array_count
        elif attr == 'CRISPR_array_count':
            val = 0
            if 'non_coding_features' in genome_data:
                for f in genome_data['non_coding_features']:
                    val += _check_feature_func (f, ['CRISPR region'])

        else:
            raise ValueError ('wrong attr type for get_genome_attribute()')
            
        return str(val)
    
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.token = os.environ['KB_AUTH_TOKEN']
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.serviceWizardURL = config['service-wizard-url']

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
#        if self.callbackURL == None:
#            self.callbackURL = os.environ['SDK_CALLBACK_URL']
        if self.callbackURL is None:
            raise ValueError("SDK_CALLBACK_URL not set in environment")

        self.scratch = os.path.abspath(config['scratch'])
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

        self.indir = os.path.join(self.scratch, 'in-'+str(uuid.uuid4()))
        if not os.path.exists(self.indir):
            os.makedirs(self.indir)
            
        self.outdir = os.path.join(self.scratch, 'out-'+str(uuid.uuid4()))
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
            
        # set test status for called modules
        self.SERVICE_VER = 'release'

        # instantiate clients
        try:
            self.wsClient = workspaceService(self.workspaceURL, token=self.token)
        except Exception as e:
            raise ValueError('Unable to connect to workspace at ' + self.workspaceURL + str(e))

        try:
            self.dfuClient = DataFileUtil(self.callbackURL, token=self.token, service_ver=self.SERVICE_VER)
        except Exception as e:
            raise ValueError('Unable to instantiate dfuClient ' + str(e))

        try:
            self.reportClient = KBaseReport(self.callbackURL, token=self.token, service_ver=self.SERVICE_VER)
        except Exception as e:
            raise ValueError('Unable to instantiate reportClient ' + str(e))

        try:
            self.setAPI_Client = SetAPI(url=self.serviceWizardURL, token=self.token, service_ver=self.SERVICE_VER)
        except Exception as e:
            raise ValueError('Unable to instantiate SetAPI' + str(e))
        
        #END_CONSTRUCTOR
        pass


    def KButil_Localize_GenomeSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Localize_GenomeSet_Params"
           (KButil_Localize_GenomeSet() ** **  Method for creating Genome Set
           with all local Genomes) -> structure: parameter "workspace_name"
           of type "workspace_name" (** The workspace object refs are of
           form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name"
        :returns: instance of type "KButil_Localize_GenomeSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Localize_GenomeSet
        raise NotImplementedError
        #END KButil_Localize_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Localize_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Localize_FeatureSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Localize_FeatureSet_Params"
           (KButil_Localize_FeatureSet() ** **  Method for creating Feature
           Set with all local Genomes) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name"
        :returns: instance of type "KButil_Localize_FeatureSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Localize_FeatureSet
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Localize_FeatureSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # param checks
        required_params = ['workspace_name',
                           'input_ref'
                           ]
        self.check_params (params, required_params)


        # read FeatureSet to get local workspace ID, source object name, and list of original genome refs
        #
        self.log (console, "READING LOCAL WORKSPACE ID")
        src_featureSet_ref = params['input_ref']

        (src_featureSet,
         info,
         src_featureSet_name,
         type_name) = self.get_obj_data(src_featureSet_ref, 'featureSet')

        if type_name != 'FeatureSet':
            raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

        # Set local WSID from FeatureSet
        local_WSID = str(info[WSID_I])


        # read workspace to determine which genome objects are already present
        #
        genome_obj_type = "KBaseGenomes.Genome"
        local_genome_refs_by_name = dict()
        genome_obj_info_list = self.get_obj_info_list_from_ws_id(local_WSID,
                                                                 genome_obj_type,
                                                                 genome_obj_type)

        for info in genome_obj_info_list:
            genome_obj_ref = self.get_obj_ref_from_obj_info(info)
            (genome_obj_name, type_name) = self.get_obj_name_and_type_from_obj_info (info)
            local_genome_refs_by_name[genome_obj_name] = genome_obj_ref


        # set order for features list
        #
        self.log (console, "GETTING FEATURES ORDERING")
        src_featureSet = data
        src_element_ordering = []
        if 'element_ordering' in list(src_featureSet.keys()):
            src_element_ordering = src_featureSet['element_ordering']
        else:
            src_element_ordering = sorted(src_featureSet['elements'].keys())
        logMsg = 'features in input set {}: {}'.format(src_featureSet_ref,
                                                       len(src_element_ordering))
        self.log(console, logMsg)
        report += logMsg


        # Standardize genome refs to numerical IDs
        #
        self.log (console, "STANDARDIZING GENOME REFS")
        genome_ref_to_standardized = dict()
        standardized_genome_refs = []
        for fId in src_element_ordering:
            for src_genome_ref in src_featureSet['elements'][fId]:
                if src_genome_ref in genome_ref_to_standardized:
                    pass
                else:
                    (src_genome_obj_info,
                     src_genome_obj_name,
                     src_genome_obj_type) = self.get_obj_info(src_genome_ref, 'genome', full_type=True)

                    #acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation"]
                    acceptable_types = ["KBaseGenomes.Genome"]
                    if src_genome_obj_type not in acceptable_types:
                        raise ValueError("Input Genome of type: '" + src_genome_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))

                    standardized_src_genome_ref = self.get_obj_ref_from_obj_info(src_genome_obj_info)
                    genome_ref_to_standardized[src_genome_ref] = standardized_src_genome_ref
                    standardized_genome_refs.append(standardized_src_genome_ref)


        # Copy all non-local genomes to local workspace
        #
        self.log (console, "COPYING NON-LOCAL GENOMES TO LOCAL WORKSPACE")
        src2dst_genome_refs = dict()
        objects_created = []
        local_genome_cnt = 0
        non_local_genome_cnt = 0
        for src_genome_ref in standardized_genome_refs:
            this_WSID = str(src_genome_ref.split('/')[0])
            if this_WSID == local_WSID:
                src2dst_genome_refs[src_genome_ref] = src_genome_ref
            else:
                (src_genome_obj_data,
                 src_genome_obj_info,
                 src_genome_obj_name,
                 type_name) = self.get_obj_data(src_genome_ref, 'genome')

                if src_genome_obj_name in local_genome_refs_by_name:
                    src2dst_genome_refs[src_genome_ref] = local_genome_refs_by_name[src_genome_obj_name]
                    local_genome_cnt += 1
                    continue
                non_local_genome_cnt += 1

                # set provenance
                input_ws_obj_refs = [src_featureSet_ref, src_genome_ref]
                provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Localize_FeatureSet')

                # Save object
                src_genome_obj_ref = self.get_obj_ref_from_obj_info(src_genome_obj_info)
                self.log(console, "SAVING GENOME "+src_genome_obj_ref+" to workspace "+str(params['workspace_name'])+" (ws."+str(local_WSID)+")")
                dst_genome_obj_data = src_genome_obj_data
                (dst_genome_obj_name, type_name) = self.get_obj_name_and_type_from_obj_info (src_genome_obj_info)
                dst_genome_obj_info = self.wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {
                            'type': 'KBaseGenomes.Genome',
                            'data': dst_genome_obj_data,
                            'name': dst_genome_obj_name,
                            'meta': {},
                            'provenance': provenance
                        }
                    ]})[0]
                dst_standardized_genome_ref = self.get_obj_ref_from_obj_info(dst_genome_obj_info)
                src2dst_genome_refs[src_genome_ref] = dst_standardized_genome_ref
                objects_created.append({'ref': dst_standardized_genome_ref,
                                        'description': 'localized '+dst_genome_obj_name})


        # Build Localized FeatureSet with local genome_refs
        #
        if non_local_genome_cnt == 0 and local_genome_cnt == 0:
            self.log (console, "NO NON-LOCAL GENOME REFS FOUND")
        else:
            self.log (console, "BUILDING LOCAL FEATURESET")
            dst_featureSet_data = dict()
            dst_featureSet_data['desc'] = src_featureSet['desc']+' - localized'
            dst_featureSet_data['element_ordering'] = src_element_ordering
            dst_featureSet_data['elements'] = dict()
            for fId in src_element_ordering:
                dst_genome_refs = []
                for orig_src_genome_ref in src_featureSet[fId]:
                    standardized_src_genome_ref = genome_ref_to_standardized[orig_src_genome_ref]
                    dst_genome_refs.append(src2dst_genome_refs[standardized_src_genome_ref])
                dst_featureSet_data['elements'][fId] = dst_genome_refs


            # Overwrite input FeatureSet object with local genome refs
            dst_featureSet_name = src_featureSet_name

            # set provenance
            input_ws_obj_refs = [src_featureSet_ref]
            provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Localize_FeatureSet')

            # save output obj
            dst_featureSet_info = self.wsClient.save_objects({
                'workspace': params['workspace_name'],
                'objects': [
                    {
                        'type': 'KBaseCollections.FeatureSet',
                        'data': output_FeatureSet,
                        'name': dst_featureSet_name,
                        'meta': {},
                        'provenance': provenance
                    }
                ]})[0]
            objects_created.append({'ref': params['workspace_name']+'/'+dst_featureSet_name,
                                    'description': 'localized FeatureSet'})


        # build output report object
        self.log(console, "BUILDING REPORT")

        total_genomes_cnt = len(standardized_genome_refs)
        if non_local_genome_cnt > 0 or local_genome_cnt > 0:
            final_msg = []
            final_msg.append("Total genomes in FeatureSet: " + str(total_genome_cnt))
            final_msg.append("Non-local genomes copied over: " + str(non_local_genome_cnt))
            final_msg.append("Local genomes with remote references: " + str(local_genome_cnt))
            logMsg = "\n".join(final_msg)
            self.log(console, logMsg)
            report += logMsg
            reportObj = {
                'objects_created': objects_created,
                'text_message': report
            }
        else:
            report += "NO NON-LOCAL GENOMES FOUND.  NO NEW FEATURESET CREATED."
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Localize_FeatureSet DONE")
        #END KButil_Localize_FeatureSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Localize_FeatureSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Merge_FeatureSet_Collection(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Merge_FeatureSet_Collection_Params"
           (KButil_Merge_FeatureSet_Collection() ** **  Method for merging
           FeatureSets) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** ** 
           objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type
           "KButil_Merge_FeatureSet_Collection_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Merge_FeatureSet_Collection
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Merge_FeatureSet_Collection with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # param checks
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Merged FeatureSet'

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 2:
            self.log(console, "Must provide at least two FeatureSets")
            self.log(invalid_msgs, "Must provide at least two FeatureSets")

        # Build FeatureSet
        element_ordering = []
        elements = {}
        featureSet_seen = dict()
        feature_seen    = dict()
        input_feature_cnt = dict()
        merged_feature_cnt = 0
        for featureSet_ref in params['input_refs']:
            if featureSet_ref not in list(featureSet_seen.keys()):
                featureSet_seen[featureSet_ref] = True
                input_feature_cnt[featureSet_ref] = 0
            else:
                self.log(console, "repeat featureSet_ref: '" + featureSet_ref + "'")
                self.log(invalid_msgs, "repeat featureSet_ref: '" + featureSet_ref + "'")
                continue

            (this_featureSet,
             info,
             obj_name,
             type_name) = self.get_obj_data(featureSet_ref, 'featureSet')

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            this_element_ordering = []
            if 'element_ordering' in list(this_featureSet.keys()):
                this_element_ordering = this_featureSet['element_ordering']
            else:
                this_element_ordering = sorted(this_featureSet['elements'].keys())
            logMsg = 'features in input set {}: {}'.format(featureSet_ref,
                                                           len(this_element_ordering))
            self.log(console, logMsg)

            for fId in this_element_ordering:
                if not elements.get(fId):
                    elements[fId] = []
                    element_ordering.append(fId)
                for genome_ref in this_featureSet['elements'][fId]:
                    input_feature_cnt[featureSet_ref] += 1
                    unique_fId = genome_ref+'-'+fId
                    if not feature_seen.get(unique_fId):
                        elements[fId].append(genome_ref)
                        merged_feature_cnt += 1
                        feature_seen[unique_fId] = True
            report += 'features in input set ' + featureSet_ref + ': ' + str(
                input_feature_cnt[featureSet_ref]) + "\n"
                
        # set provenance
        input_ws_obj_refs = params['input_refs']
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Merge_FeatureSet_Collection')

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING FEATURESET")
            output_FeatureSet = {'description': params['desc'],
                                 'element_ordering': element_ordering,
                                 'elements': elements}

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{
                                                           'type': 'KBaseCollections.FeatureSet',
                                                           'data': output_FeatureSet,
                                                           'name': params['output_name'],
                                                           'meta': {},
                                                           'provenance': provenance}]})[0]
            
        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "features in output set " + params['output_name'] + ": "
                     + str(merged_feature_cnt))
            report += 'features in output set ' + params['output_name'] + ': '
            report += str(merged_feature_cnt) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Merge_FeatureSet_Collection'}],
                'text_message': report
            }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Merge_FeatureSet_Collection DONE")
        #END KButil_Merge_FeatureSet_Collection

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Merge_FeatureSet_Collection return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Slice_FeatureSets_by_Genomes(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Slice_FeatureSets_by_Genomes_Params"
           (KButil_Slice_FeatureSets_by_Genomes() ** **  Method for Slicing a
           FeatureSet or FeatureSets by a Genome, Genomes, or GenomeSet) ->
           structure: parameter "workspace_name" of type "workspace_name" (**
           The workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_featureSet_refs" of type "data_obj_ref",
           parameter "input_genome_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type
           "KButil_Slice_FeatureSets_by_Genomes_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Slice_FeatureSets_by_Genomes
        console = []
        invalid_msgs = []
        self.log(console, 'Running Slice_FeatureSets_by_Genomes with params=')
        self.log(console, "\n" + pformat(params))
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_featureSet_refs',
                           'input_genome_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced FeatureSet'


        # clean input_feature_refs
        clean_input_refs = []
        for ref in params['input_featureSet_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_featureSet_refs'] = clean_input_refs

        # clean input_genome_refs
        clean_input_refs = []
        for ref in params['input_genome_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_genome_refs'] = clean_input_refs


        # Standardize genome refs so string comparisons are valid (only do requested genomes)
        #
        genome_ref_to_standardized                 = dict()
        genome_ref_from_standardized_in_input_flag = dict()
        for this_genome_ref in params['input_genome_refs']:

            (genome_obj_info,
             genome_obj_name,
             genome_obj_type) = self.get_obj_info(this_genome_ref, 'genome', full_type=True)
            
            acceptable_types = ["KBaseGenomes.Genome", "KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
            if genome_obj_type not in acceptable_types:
                raise ValueError("Input Genome of type: '" + genome_obj_type +
                                 "'.  Must be one of " + ", ".join(acceptable_types))

            this_standardized_genome_ref = self.get_obj_ref_from_obj_info(genome_obj_info)
            genome_ref_to_standardized[this_genome_ref] = this_standardized_genome_ref
            genome_ref_from_standardized_in_input_flag[this_standardized_genome_ref] = True


        # Build FeatureSets
        #
        featureSet_seen = dict()
        featureSet_genome_ref_to_standardized = dict()  # have to map genome refs in featureSets also because might be mixed WS_ID-WS_NAME/OBJID-OBJNAME and not exactly correspond with input genome refs
        feature_list_lens = []
        objects_created = []

        for featureSet_ref in params['input_featureSet_refs']:
            if featureSet_ref not in list(featureSet_seen.keys()):
                featureSet_seen[featureSet_ref] = 1
            else:
                self.log(console, "repeat featureSet_ref: '" + featureSet_ref + "'")
                self.log(invalid_msgs, "repeat featureSet_ref: '" + featureSet_ref + "'")
                continue

            (this_featureSet,
             info,
             this_featureSet_obj_name,
             type_name) = self.get_obj_data(featureSet_ref, 'featureSet')

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            this_element_ordering = []
            if 'element_ordering' in list(this_featureSet.keys()):
                this_element_ordering = this_featureSet['element_ordering']
            else:
                this_element_ordering = sorted(this_featureSet['elements'].keys())
            logMsg = 'features in input set {}: {}'.format(featureSet_ref,
                                                           len(this_element_ordering))
            self.log(console, logMsg)


            # Build sliced FeatureSet
            #
            self.log (console, "BUILDING SLICED FEATURESET\n")
            self.log (console, "Slicing out genomes "+("\n".join(params['input_genome_refs'])))
            element_ordering = []
            elements = {}
            for fId in this_element_ordering:
                feature_hit = False
                genomes_retained = []
                for this_genome_ref in this_featureSet['elements'][fId]:
                    genome_hit = False

                    if this_genome_ref in genome_ref_to_standardized:  # The KEY line
                        genome_hit = True
                        standardized_genome_ref = genome_ref_to_standardized[this_genome_ref]
                    elif this_genome_ref in featureSet_genome_ref_to_standardized:
                        standardized_genome_ref = featureSet_genome_ref_to_standardized[this_genome_ref]
                        if standardized_genome_ref in genome_ref_from_standardized_in_input_flag:
                            genome_hit = True
                    else:  # get standardized genome_ref
                        (genome_obj_info,
                         genome_obj_name,
                         genome_obj_type) = self.get_obj_info(this_genome_ref, 'genome', full_type=True)

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
                        if genome_obj_type not in acceptable_types:
                            raise ValueError("Input Genome of type: '" + genome_obj_type +
                                             "'.  Must be one of " + ", ".join(acceptable_types))

                        standardized_genome_ref = self.get_obj_ref_from_obj_info(genome_obj_info)
                        featureSet_genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref
                        if standardized_genome_ref in genome_ref_from_standardized_in_input_flag:
                            genome_hit = True

                    if genome_hit:
                        feature_hit = True
                        genomes_retained.append(standardized_genome_ref)

                if feature_hit:
                    element_ordering.append(fId)
                    elements[fId] = genomes_retained
            logMsg = 'features in sliced output set: {}'.format(len(element_ordering))
            self.log(console, logMsg)


            # Save output FeatureSet
            #
            if len(element_ordering) == 0:
                report += 'no features for requested genomes in FeatureSet '+str(featureSet_ref)
                feature_list_lens.append(0)
            else:
                # set provenance
                self.log(console, "SETTING PROVENANCE")
                input_ws_obj_refs = [featureSet_ref]
                input_ws_obj_refs.extend(params['input_genome_refs'])
                provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Slice_FeatureSets_by_Genome')

                # Store output object
                if len(invalid_msgs) == 0:
                    self.log(console, "SAVING FEATURESET")
                    output_FeatureSet = {'description': params['desc'],
                                         'element_ordering': element_ordering,
                                         'elements': elements}

                    output_name = params['output_name']
                    if len(params['input_featureSet_refs']) > 1:
                        output_name += '-' + this_featureSet_obj_name

                    new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                          'objects': [{
                                                              'type': 'KBaseCollections.FeatureSet',
                                                              'data': output_FeatureSet,
                                                              'name': output_name,
                                                              'meta': {},
                                                              'provenance': provenance}]})[0]

                    feature_list_lens.append(len(element_ordering))
                    objects_created.append({'ref': params['workspace_name'] + '/' + output_name,
                                            'description': params['desc']})


        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            obj_i = -1
            for output_i,list_len in enumerate(feature_list_lens):
                if feature_list_lens[output_i] == 0:
                    report += 'No features for requested genomes in featureSet '+str(params['input_featureSet_refs'][output_i])+"\n"
                else:
                    obj_i += 1
                    report += 'features in output set ' + objects_created[obj_i]['ref'] + ': '
                    report += str(feature_list_lens[output_i]) + "\n"
            reportObj = {
                'objects_created': objects_created,
                'text_message': report
            }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Slice_FeatureSets_by_Genomes DONE")
        #END KButil_Slice_FeatureSets_by_Genomes

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Slice_FeatureSets_by_Genomes return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Logical_Slice_Two_FeatureSets(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Logical_Slice_Two_FeatureSets_Params"
           (KButil_Logical_Slice_Two_FeatureSets() ** **  Method for Slicing
           Two FeatureSets by Venn overlap) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_featureSet_ref_A" of type "data_obj_ref",
           parameter "input_featureSet_ref_B" of type "data_obj_ref",
           parameter "operator" of String, parameter "desc" of String,
           parameter "output_name" of type "data_obj_name"
        :returns: instance of type
           "KButil_Logical_Slice_Two_FeatureSets_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Logical_Slice_Two_FeatureSets
        console = []
        invalid_msgs = []
        self.log(console, 'Running Logical_Slice_Two_FeatureSets with params=')
        self.log(console, "\n" + pformat(params))
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''
        genome_id_feature_id_delim = ".f:"


        # check params
        required_params = ['workspace_name',
                           'operator',
                           'input_featureSet_ref_A',
                           'input_featureSet_ref_B',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced FeatureSet'


        # Get FeatureSets
        #
        FeatureSet = dict()
        FeatureSet['A'] = dict()
        FeatureSet['B'] = dict()
        input_featureSet_refs = dict()
        input_featureSet_refs['A'] = params['input_featureSet_ref_A']
        input_featureSet_refs['B'] = params['input_featureSet_ref_B']
        input_featureSet_names = dict()
        for set_id in ['A','B']:

            (this_featureSet,
             info,
             this_featureSet_obj_name,
             type_name) = self.get_obj_data(input_featureSet_refs[set_id], 'featureSet')

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            input_featureSet_names[set_id] = this_featureSet_obj_name
            FeatureSet[set_id] = this_featureSet
            if 'element_ordering' not in list(this_featureSet.keys()):
                FeatureSet[set_id]['element_ordering'] = sorted(this_featureSet['elements'].keys())
            logMsg = 'features in input set {} - {}: {}'.format(set_id,
                                                                this_featureSet_obj_name,
                                                           len(FeatureSet[set_id]['element_ordering']))
            self.log(console, logMsg)
            report += logMsg+"\n"
            

        # Store A and B genome + fid hits
        #
        genome_feature_present = dict()
        genome_feature_present['A'] = dict()
        genome_feature_present['B'] = dict()
        featureSet_genome_ref_to_standardized = dict()  # must use standardized genome_refs

        for set_id in ['A','B']:
            for fId in FeatureSet[set_id]['element_ordering']:
                feature_standardized_genome_refs = []
                for this_genome_ref in FeatureSet[set_id]['elements'][fId]:

                    if this_genome_ref in featureSet_genome_ref_to_standardized:
                        standardized_genome_ref_noVer = featureSet_genome_ref_to_standardized[this_genome_ref]
                    else:  # get standardized genome_ref
                        (genome_obj_info,
                         genome_obj_name,
                         genome_obj_type) = self.get_obj_info(this_genome_ref, 'genome', full_type=True)

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation","KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
                        if genome_obj_type not in acceptable_types:
                            raise ValueError("Input Genome of type: '" + genome_obj_type +
                                             "'.  Must be one of " + ", ".join(acceptable_types))

                        standardized_genome_ref_noVer = '{}/{}'.format(genome_obj_info[WSID_I],
                                                                       genome_obj_info[OBJID_I])
                        featureSet_genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref_noVer
                    feature_standardized_genome_refs.append(standardized_genome_ref_noVer)  # standardize list
                    combo_id = standardized_genome_ref_noVer + genome_id_feature_id_delim + fId
                    genome_feature_present[set_id][combo_id] = True
                    self.log(console,"Set {} contains {}".format(set_id,combo_id))
                FeatureSet[set_id]['elements'][fId] = feature_standardized_genome_refs


        # Build sliced FeatureSet
        #
        self.log (console, "BUILDING SLICED FEATURESET\n")
        output_element_ordering = []
        output_elements = dict()
        if params['operator'] == 'yesA_yesB' or params['operator'] == 'yesA_noB':
            input_element_ordering = FeatureSet['A']['element_ordering']
            fwd_set_id = 'A'
            rev_set_id = 'B'
        else:
            input_element_ordering = FeatureSet['B']['element_ordering']
            fwd_set_id = 'B'
            rev_set_id = 'A'

        for fId in input_element_ordering:
            feature_hit = False
            genomes_retained = []
            for this_genome_ref_noVer in FeatureSet[fwd_set_id]['elements'][fId]:
                combo_id = this_genome_ref_noVer + genome_id_feature_id_delim + fId
                self.log (console, "\t"+'checking set {} genome+fid: {}'.format(fwd_set_id,combo_id))

                if params['operator'] == 'yesA_yesB':
                    if genome_feature_present[rev_set_id].get(combo_id):
                        feature_hit = True
                        genomes_retained.append(this_genome_ref_noVer)
                        self.log(console, "keeping feature {}".format(combo_id))
                else:
                    if not genome_feature_present[rev_set_id].get(combo_id):
                        feature_hit = True
                        genomes_retained.append(this_genome_ref_noVer)
                        self.log(console, "keeping feature {}".format(combo_id))

            if feature_hit:
                output_element_ordering.append(fId)
                output_elements[fId] = genomes_retained
        logMsg = 'features in sliced output set: {}'.format(len(output_element_ordering))
        self.log(console, logMsg)


        # Save output FeatureSet
        #
        objects_created = []

        # set provenance
        input_ws_obj_refs = [input_featureSet_refs['A'], input_featureSet_refs['B']]
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Logical_Slice_Two_FeatureSets')

        if len(output_element_ordering) == 0:
            report += 'no features to output under operator '+params['operator']+"\n"

        else:

            # Store output object
            if len(invalid_msgs) == 0:
                self.log(console, "SAVING FEATURESET")
                output_FeatureSet = {'description': params['desc'],
                                     'element_ordering': output_element_ordering,
                                     'elements': output_elements}

                output_name = params['output_name']

                new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                      'objects': [{
                                                          'type': 'KBaseCollections.FeatureSet',
                                                          'data': output_FeatureSet,
                                                          'name': output_name,
                                                          'meta': {},
                                                          'provenance': provenance}]})[0]

                objects_created.append({'ref': params['workspace_name'] + '/' + output_name,
                                        'description': params['desc']})

        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "features in output set " + params['output_name'] + ": "
                     + str(len(output_element_ordering)))
            report += 'features in output set ' + params['output_name'] + ': '
            report += str(len(output_element_ordering)) + "\n"
            reportObj = {
                'objects_created': objects_created,
                'text_message': report
            }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Logical_Slice_Two_FeatureSets DONE")
        #END KButil_Logical_Slice_Two_FeatureSets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Logical_Slice_Two_FeatureSets return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Logical_Slice_Two_AssemblySets(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Logical_Slice_Two_AssemblySets_Params"
           (KButil_Logical_Slice_Two_AssemblySets() ** **  Method for Slicing
           Two AssemblySets by Venn overlap) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_assemblySet_ref_A" of type "data_obj_ref",
           parameter "input_assemblySet_ref_B" of type "data_obj_ref",
           parameter "operator" of String, parameter "desc" of String,
           parameter "output_name" of type "data_obj_name"
        :returns: instance of type
           "KButil_Logical_Slice_Two_AssemblySets_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Logical_Slice_Two_AssemblySets
        console = []
        invalid_msgs = []
        self.log(console, 'Running Logical_Slice_Two_AssemblySets with params=')
        self.log(console, "\n" + pformat(params))
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''


        # check params
        required_params = ['workspace_name',
                           'operator',
                           'input_assemblySet_ref_A',
                           'input_assemblySet_ref_B',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced AssemblySet'


        # Get AssemblySets
        #
        AssemblySet = dict()
        AssemblySet['A'] = dict()
        AssemblySet['B'] = dict()
        input_assemblySet_refs = dict()
        input_assemblySet_refs['A'] = params['input_assemblySet_ref_A']
        input_assemblySet_refs['B'] = params['input_assemblySet_ref_B']
        input_assemblySet_names = dict()
        for set_id in ['A','B']:

            (this_assemblySet,
             info,
             this_assemblySet_obj_name,
             type_name) = self.get_obj_data(input_assemblySet_refs[set_id], 'assemblySet')

            if type_name != 'AssemblySet':
                raise ValueError("Bad Type:  Should be AssemblySet instead of '" + type_name + "'")

            input_assemblySet_names[set_id] = this_assemblySet_obj_name
            AssemblySet[set_id] = this_assemblySet
            logMsg = 'assemblies in input set {} - {}: {}'.format(set_id,
                                                                  this_assemblySet_obj_name,
                                                           len(AssemblySet[set_id]['items']))
            self.log(console, logMsg)
            report += logMsg+"\n"
            

        # Store A and B assemblies
        #
        assembly_obj_present = dict()
        assembly_obj_present['A'] = dict()
        assembly_obj_present['B'] = dict()
        assembly_ref_to_standardized = dict()  # must use standardized assembly_refs

        for set_id in ['A','B']:
            new_items = []
            for item in AssemblySet[set_id]['items']:
                standardized_assembly_refs = []
                this_assembly_ref = item['ref']
                
                if this_assembly_ref in assembly_ref_to_standardized:
                    standardized_assembly_ref_noVer = assembly_ref_to_standardized[this_assembly_ref]
                else:  # get standardized assembly_ref
                    (assembly_obj_info,
                     assembly_obj_name,
                     assembly_obj_type) = self.get_obj_info(this_assembly_ref, 'assembly', full_type=True)

                    acceptable_types = ["KBaseGenomeAnnotations.Assembly"]
                    if assembly_obj_type not in acceptable_types:
                        raise ValueError("Input Assembly of type: '" + assembly_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))

                    standardized_assembly_ref_noVer = '{}/{}'.format(assembly_obj_info[WSID_I],
                                                                     assembly_obj_info[OBJID_I])
                    assembly_ref_to_standardized[this_assembly_ref] = standardized_assembly_ref_noVer
                standardized_assembly_refs.append(standardized_assembly_ref_noVer)  # standardize list
                assembly_obj_present[set_id][standardized_assembly_ref_noVer] = True
                new_items.append({'ref':standardized_assembly_ref_noVer,'label':item['label']})
                self.log(console,"Set {} contains {}".format(set_id,standardized_assembly_ref_noVer))
            AssemblySet[set_id]['items'] = new_items


        # Build sliced AssemblySet
        #
        self.log (console, "BUILDING SLICED ASSEMBLYSET")
        output_items = []
        if params['operator'] == 'yesA_yesB' or params['operator'] == 'yesA_noB':
            input_items = AssemblySet['A']['items']
            fwd_set_id = 'A'
            rev_set_id = 'B'
        else:
            input_items = AssemblySet['B']['items']
            fwd_set_id = 'B'
            rev_set_id = 'A'

        for item in input_items:
            self.log (console, 'checking assembly {} from set {}'.format(item['ref'],fwd_set_id))
            this_standardized_assembly_ref_noVer = item['ref']
            if params['operator'] == 'yesA_yesB':
                if assembly_obj_present[rev_set_id].get(this_standardized_assembly_ref_noVer):
                    self.log(console, "keeping assembly {}".format(item['ref']))
                    output_items.append(item)
            else:
                if not assembly_obj_present[rev_set_id].get(this_standardized_assembly_ref_noVer):
                    self.log(console, "keeping assembly {}".format(item['ref']))
                    output_items.append(item)
        logMsg = 'assemblies in sliced output set: {}'.format(len(output_items))
        self.log(console, logMsg)


        # Save output AssemblySet
        #
        objects_created = []

        if len(output_items) == 0:
            report += 'no assemblies to output under operator '+params['operator']+"\n"
        else:
            if params.get('desc'):
                output_desc = params['desc']
            else:
                output_desc = 'Venn slice '+params['operator']+' of AssemblySets '+input_assemblySet_names['A']+' and '+input_assemblySet_names['B']
            output_assemblySet_obj = { 'description': output_desc,
                                       'items': output_items
                                     }
            output_assemblySet_name = params['output_name']
            try:
                output_assemblySet_ref = self.setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                        'output_object_name': output_assemblySet_name,
                                                                        'data': output_assemblySet_obj
                                                                        })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(output_items) > 0:
            self.log(console, "assemblies in output set " + params['output_name'] + ": "
                     + str(len(output_items)))
            report += 'assemblies in output set ' + params['output_name'] + ': '
            report += str(len(output_items)) + "\n"
            reportObj = {
                'objects_created': objects_created,
                'text_message': report
            }
        else:
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Logical_Slice_Two_AssemblySets DONE")
        #END KButil_Logical_Slice_Two_AssemblySets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Logical_Slice_Two_AssemblySets return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Logical_Slice_Two_GenomeSets(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Logical_Slice_Two_GenomeSets_Params"
           (KButil_Logical_Slice_Two_GenomeSets() ** **  Method for Slicing
           Two AssemblySets by Venn overlap) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_genomeSet_ref_A" of type "data_obj_ref",
           parameter "input_genomeSet_ref_B" of type "data_obj_ref",
           parameter "operator" of String, parameter "desc" of String,
           parameter "output_name" of type "data_obj_name"
        :returns: instance of type
           "KButil_Logical_Slice_Two_GenomeSets_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Logical_Slice_Two_GenomeSets
        console = []
        invalid_msgs = []
        self.log(console, 'Running Logical_Slice_Two_GenomeSets with params=')
        self.log(console, "\n" + pformat(params))
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''


        # check params
        required_params = ['workspace_name',
                           'operator',
                           'input_genomeSet_ref_A',
                           'input_genomeSet_ref_B',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced GenomeSet'


        # Get GenomeSets
        #
        GenomeSet_element_refs = dict()
        input_genomeSet_refs = dict()
        input_genomeSet_refs['A'] = params['input_genomeSet_ref_A']
        input_genomeSet_refs['B'] = params['input_genomeSet_ref_B']
        input_genomeSet_names = dict()
        for set_id in ['A','B']:

            (this_genomeSet,
             info,
             this_genomeSet_obj_name,
             type_name) = self.get_obj_data(input_genomeSet_refs[set_id], 'genomeSet')

            input_genomeSet_names[set_id] = this_genomeSet_obj_name;

            if type_name != 'GenomeSet':
                raise ValueError("Bad Type:  Should be GenomeSet instead of '" + type_name + "'")

            GenomeSet_element_refs[set_id] = []
            for genome_id in sorted(this_genomeSet['elements'].keys()):
                GenomeSet_element_refs[set_id].append(this_genomeSet['elements'][genome_id]['ref'])
            logMsg = 'genomes in input set {} - {}: {}'.format(set_id,
                                                               this_genomeSet_obj_name,
                                                          len(GenomeSet_element_refs[set_id]))
            self.log(console, logMsg)
            report += logMsg+"\n"


        # Store A and B genome + fid hits
        #
        genome_obj_present = dict()
        genome_obj_present['A'] = dict()
        genome_obj_present['B'] = dict()
        genome_ref_to_standardized = dict()  # must use standardized genome_refs

        for set_id in ['A','B']:
            new_element_refs = []
            for this_genome_ref in GenomeSet_element_refs[set_id]:
                standardized_genome_refs = []
                
                if this_genome_ref in genome_ref_to_standardized:
                    standardized_genome_ref_noVer = genome_ref_to_standardized[this_genome_ref]
                else:  # get standardized genome_ref
                    (genome_obj_info,
                     genome_obj_name,
                     genome_obj_type) = self.get_obj_info(this_genome_ref, 'genome', full_type=True)

                    acceptable_types = ["KBaseGenomes.Genome","KBaseGenomeAnnotations.GenomeAnnotation"]
                    if genome_obj_type not in acceptable_types:
                        raise ValueError("Input Genome of type: '" + genome_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))

                    standardized_genome_ref_noVer = '{}/{}'.format(genome_obj_info[WSID_I],
                                                                   genome_obj_info[OBJID_I])
                    genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref_noVer
                standardized_genome_refs.append(standardized_genome_ref_noVer)  # standardize list
                genome_obj_present[set_id][standardized_genome_ref_noVer] = True
                new_element_refs.append(standardized_genome_ref_noVer)
                self.log(console,"Set {} contains {}".format(set_id,standardized_genome_ref_noVer))
            GenomeSet_element_refs[set_id] = new_element_refs


        # Build sliced GenomeSet
        #
        self.log (console, "BUILDING SLICED GENOMESET")
        output_items = []
        if params['operator'] == 'yesA_yesB' or params['operator'] == 'yesA_noB':
            input_element_refs = GenomeSet_element_refs['A']
            fwd_set_id = 'A'
            rev_set_id = 'B'
        else:
            input_element_refs = GenomeSet_element_refs['B']
            fwd_set_id = 'B'
            rev_set_id = 'A'

        for this_standardized_genome_ref_noVer in input_element_refs:
            self.log (console, 'checking set {} genome {}'.format(set_id,this_standardized_genome_ref_noVer))
            if params['operator'] == 'yesA_yesB':
                if genome_obj_present[rev_set_id].get(this_standardized_genome_ref_noVer):
                    output_items.append(this_standardized_genome_ref_noVer)
                    self.log(console, "keeping genome {}".format(this_standardized_genome_ref_noVer))
            else:
                if not genome_obj_present[rev_set_id].get(this_standardized_genome_ref_noVer):
                    output_items.append(this_standardized_genome_ref_noVer)
                    self.log(console, "keeping genome {}".format(this_standardized_genome_ref_noVer))
        logMsg = 'genomes in sliced output set: {}'.format(len(output_items))
        self.log(console, logMsg)


        # Save output GenomeSet
        #
        objects_created = []

        # set provenance
        input_ws_obj_refs = [input_genomeSet_refs['A'], input_genomeSet_refs['B']]
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Logical_Slice_Two_GenomeSets')

        if len(output_items) == 0:
            report += 'no genomes to output under operator '+params['operator']+"\n"
        else:
            # KBaseSearch.GenomeSet form is a dict of elements, not a list of items
            output_elements = dict();
            for genome_ref in sorted(output_items):
                output_elements[genome_ref] = {'ref':genome_ref}
                
            if params.get('desc'):
                output_desc = params['desc']
            else:
                output_desc = 'Venn slice '+params['operator']+' of GenomeSets '+input_genomeSet_names['A']+' and '+input_genomeSet_names['B']
            output_genomeSet_obj = { 'description': output_desc,
                                     'elements': output_elements
            }
            output_genomeSet_name = params['output_name']

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                  'objects': [{
                                                      'type': 'KBaseSearch.GenomeSet',
                                                      'data': output_genomeSet_obj,
                                                      'name': output_genomeSet_name,
                                                      'meta': {},
                                                      'provenance': provenance}]})[0]

            objects_created.append({'ref': params['workspace_name'] + '/' + output_genomeSet_name,
                                    'description': output_desc})

            

        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(output_items) > 0:
            self.log(console, "assemblies in output set " + params['output_name'] + ": "
                     + str(len(output_items)))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(output_items)) + "\n"
            reportObj = {
                'objects_created': objects_created,
                'text_message': report
            }
        else:
            reportObj = {
                'objects_created': [],
                'text_message': report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Logical_Slice_Two_GenomeSets DONE")
        #END KButil_Logical_Slice_Two_GenomeSets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Logical_Slice_Two_GenomeSets return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Merge_GenomeSets(self, ctx, params):
        """
        :param params: instance of type "KButil_Merge_GenomeSets_Params"
           (KButil_Merge_GenomeSets() ** **  Method for merging GenomeSets)
           -> structure: parameter "workspace_name" of type "workspace_name"
           (** The workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Merge_GenomeSets_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Merge_GenomeSets
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Merge_GenomeSets with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Merged GenomeSet'

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 2:
            self.log(console, "Must provide at least two GenomeSets")
            self.log(invalid_msgs, "Must provide at least two GenomeSets")

        # set provenance
        self.log(console, "SETTING PROVENANCE")
        input_ws_obj_refs = params['input_refs']
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Merge_GenomeSets')

        # Build GenomeSet
        #
        elements = dict()

        # Add Genomes from GenomeSets
        for input_genomeset_ref in params['input_refs']:

            (genomeSet,
             info,
             this_genomeSet_obj_name,
             type_name) = self.get_obj_data(input_genomeset_ref, 'genomeSet')

            if type_name != 'GenomeSet':
                raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")

            for gId in list(genomeSet['elements'].keys()):
                old_genomeRef = genomeSet['elements'][gId]['ref']
                (this_obj_info,
                 this_obj_name,
                 this_obj_type) = self.get_obj_info(old_genomeRef, 'genome')

                standardized_genomeRef = self.get_obj_ref_from_obj_info_noVer(this_obj_info)
                new_gId = standardized_genomeRef
                if not elements.get(new_gId):
                    elements[new_gId] = dict()
                    elements[new_gId]['ref'] = standardized_genomeRef  # the key line
                    self.log(console, "adding element " + new_gId + " : " + standardized_genomeRef)

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements
                                }

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                                    'data': output_GenomeSet,
                                                                    'name': params['output_name'],
                                                                    'meta': {},
                                                                    'provenance': provenance
                                                                  }]
                                                       })[0]
            
        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                              str(len(list(elements.keys()))))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(list(elements.keys()))) + "\n"
            ref = params['workspace_name'] + '/' + params['output_name']
            reportObj = {'objects_created': [{'ref': ref,
                                              'description': 'KButil_Merge_GenomeSets'}],
                         'text_message': report
                         }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report
                         }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Merge_GenomeSets DONE")
        #END KButil_Merge_GenomeSets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Merge_GenomeSets return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Build_GenomeSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Build_GenomeSet_Params"
           (KButil_Build_GenomeSet() ** **  Method for creating a GenomeSet)
           -> structure: parameter "workspace_name" of type "workspace_name"
           (** The workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Build_GenomeSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Build_GenomeSet
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Build_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Built GenomeSet'

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 1:
            self.log(console, "Must provide at least one Genome")
            self.log(invalid_msgs, "Must provide at least one Genome")

        # Build GenomeSet
        #
        elements = {}
        genome_seen = dict()

        for genomeRef in params['input_refs']:

            if not genome_seen.get(genomeRef):
                genome_seen[genomeRef] = True

                (genomeObj,
                 info,
                 obj_name,
                 type_name) = self.get_obj_data(genomeRef, 'genome')

                if type_name != 'Genome' and type_name != 'GenomeAnnotation':
                    errMsg = "Bad Type: Should be Genome or GenomeAnnotation not '{}' for ref: '{}'"
                    raise ValueError(errMsg.format(type_name, genomeRef))

                if type_name == 'Genome':
                    genome_id = genomeObj['id']
                else:
                    genome_id = genomeObj['genome_annotation_id']
                genome_sci_name = genomeObj['scientific_name']

                if genomeRef not in list(elements.keys()):
                    elements[genomeRef] = dict()
                elements[genomeRef]['ref'] = genomeRef  # the key line
                self.log(console, "adding element {} ({}) aka ({}): {}".format(obj_name,
                                                                               genome_sci_name,
                                                                               genome_id,
                                                                               genomeRef))

        # set provenance
        self.log(console, "SETTING PROVENANCE")
        input_ws_obj_refs = params['input_refs']
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Build_GenomeSet')

        # Store output object
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                                    'data': output_GenomeSet,
                                                                    'name': params['output_name'],
                                                                    'meta': {},
                                                                    'provenance': provenance}]})[0]

        # build output report object
        #
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] +
                              ": " + str(len(list(elements.keys()))))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(list(elements.keys()))) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Build_GenomeSet'}],
                'text_message': report
            }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Build_GenomeSet DONE")
        #END KButil_Build_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Build_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Build_GenomeSet_from_FeatureSet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Build_GenomeSet_from_FeatureSet_Params"
           (KButil_Build_GenomeSet_from_FeatureSet() ** **  Method for
           obtaining a GenomeSet from a FeatureSet) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type
           "KButil_Build_GenomeSet_from_FeatureSet_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Build_GenomeSet_from_FeatureSet
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Build_GenomeSet_from_FeatureSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_ref',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Built GenomeSet'

        # Obtain FeatureSet
        (featureSet,
         info,
         obj_name,
         type_name) = self.get_obj_data(params['input_ref'], 'featureSet')

        if type_name != 'FeatureSet':
            raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

        # Build GenomeSet
        elements = {}
        genome_seen = dict()

        for fId in list(featureSet['elements'].keys()):
            for genomeRef in featureSet['elements'][fId]:

                if not genome_seen.get(genomeRef):
                    genome_seen[genomeRef] = True

                    (genomeObj,
                     info,
                     obj_name,
                     type_name) = self.get_obj_data(genomeRef, 'genome')

                    if type_name == 'AnnotatedMetagenomeAssembly':
                        self.log(console, "SKIPPING AnnotatedMetagenomeAssembly Object "+obj_name)
                        continue
                    elif type_name != 'Genome' and type_name != 'GenomeAnnotaton':
                        errMsg = "Bad Type:  Should be Genome or GenomeAnnotation instead"
                        errMsg += " of '{}' for ref: '{}'"
                        raise ValueError(errMsg.format(type_name, genomeRef))

                    if type_name == 'Genome':
                        genome_id = genomeObj['id']
                    else:
                        genome_id = genomeObj['genome_annotation_id']
                    genome_sci_name = genomeObj['scientific_name']

                    #if not genome_id in elements.keys():
                    #    elements[genome_id] = dict()
                    #elements[genome_id]['ref'] = genomeRef  # the key line
                    if genomeRef not in list(elements.keys()):
                        elements[genomeRef] = dict()
                    elements[genomeRef]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element {} ({}/{}) : {}".format(obj_name,
                                                                              genome_sci_name,
                                                                              genome_id,
                                                                              genomeRef))

        # set provenance
        self.log(console, "SETTING PROVENANCE")
        input_ws_obj_refs = [params['input_ref']]
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Build_GenomeSet_from_FeatureSet')

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                                    'data': output_GenomeSet,
                                                                    'name': params['output_name'],
                                                                    'meta': {},
                                                                    'provenance': provenance}]})[0]
            
        # build output report object
        #
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                     str(len(list(elements.keys()))))
            report += 'genomes in output set {}:{}\n'.format(params['output_name'],
                                                             len(list(elements.keys())))
            ref = "{}/{}".format(params['workspace_name'], params['output_name'])
            reportObj = {'objects_created': [{'ref': ref,
                         'description': 'KButil_Build_GenomeSet_from_FeatureSet'}],
                         'text_message': report}
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Build_GenomeSet_from_FeatureSet DONE")
        #END KButil_Build_GenomeSet_from_FeatureSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Build_GenomeSet_from_FeatureSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Add_Genomes_to_GenomeSet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Add_Genomes_to_GenomeSet_Params"
           (KButil_Add_Genomes_to_GenomeSet() ** **  Method for adding a
           Genome to a GenomeSet) -> structure: parameter "workspace_name" of
           type "workspace_name" (** The workspace object refs are of form:
           ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_genome_refs" of list of type "data_obj_ref",
           parameter "input_genomeset_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Add_Genomes_to_GenomeSet_Output"
           -> structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Add_Genomes_to_GenomeSet

        # init
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Add_Genomes_to_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_genome_refs',
                           'input_genomeset_ref',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Increased GenomeSet'

        # Build GenomeSet
        elements = dict()
        query_genome_ref_order = []
        
        # add old GenomeSet
        #
        if 'input_genomeset_ref' in params and params['input_genomeset_ref'] is not None:
            (genomeSet,
             info,
             obj_name,
             type_name) = self.get_obj_data(params['input_genomeset_ref'], 'genomeSet')

            if type_name != 'GenomeSet':
                raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")

            for gId in list(genomeSet['elements'].keys()):
                genomeRef = genomeSet['elements'][gId]['ref']

                if not elements.get(genomeRef):
                    elements[genomeRef] = dict()
                    elements[genomeRef]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element " + gId + " : " + genomeRef)

                    query_genome_ref_order.append(genomeRef)
                    

        # add new genomes
        #
        genomeSet_obj_types = ["KBaseSearch.GenomeSet", "KBaseSets.GenomeSet"]
        genome_obj_types    = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.Genome"]
        tree_obj_types      = ["KBaseTrees.Tree"]
        for input_ref in params['input_genome_refs']:

            (query_genome_obj_data,
             query_genome_obj_info,
             query_genome_obj_name,
             query_genome_obj_type) = self.get_obj_data(input_ref, 'genome or genomeSet', full_type=True)

            # just a genome
            if query_genome_obj_type in genome_obj_types:
                if input_ref not in elements:
                    elements[input_ref] = dict()
                    elements[input_ref]['ref'] = input_ref  # the key line
                    self.log(console, "adding element " + input_ref)
                    query_genome_ref_order.append(input_ref)

            # handle genomeSet
            elif query_genome_obj_type in genomeSet_obj_types:
                for genome_id in sorted(query_genome_obj_data['elements'].keys()):
                    genome_ref = query_genome_obj_data['elements'][genome_id]['ref']
                    if genome_ref not in elements:
                        elements[genome_ref] = dict()
                        elements[genome_ref]['ref'] = genome_ref  # the key line
                        self.log(console, "adding element " + genome_ref)
                        query_genome_ref_order.append(genome_ref)

            # handle tree type
            elif query_genome_obj_type in tree_obj_types:
                for genome_id in sorted(query_genome_obj_data['ws_refs'].keys()):
                    genome_ref = query_genome_obj_data['ws_refs'][genome_id]['g'][0]
                    if genome_ref not in elements:
                        elements[genome_ref] = dict()
                        elements[genome_ref]['ref'] = genome_ref  # the key line
                        self.log(console, "adding element " + genome_ref)
                        query_genome_ref_order.append(genome_ref)
            else:  
                raise ValueError ("bad type for input_genome_refs")


        # set provenance
        self.log(console, "SETTING PROVENANCE")
        input_ws_obj_refs = [params['input_genomeset_ref']]
        input_ws_obj_refs.extend(params['input_genome_refs'])
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Add_Genomes_to_GenomeSet')

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{
                                                           'type': 'KBaseSearch.GenomeSet',
                                                           'data': output_GenomeSet,
                                                           'name': params['output_name'],
                                                           'meta': {},
                                                           'provenance': provenance}]})[0]

        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                     str(len(list(elements.keys()))))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(list(elements.keys()))) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Add_Genomes_to_GenomeSet'}],
                'text_message': report}
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Add_Genomes_to_GenomeSet DONE")
        #END KButil_Add_Genomes_to_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Add_Genomes_to_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Remove_Genomes_from_GenomeSet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Remove_Genomes_from_GenomeSet_Params"
           (KButil_Remove_Genomes_from_GenomeSet() ** **  Method for removing
           Genomes from a GenomeSet) -> structure: parameter "workspace_name"
           of type "workspace_name" (** The workspace object refs are of
           form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_genome_refs" of list of type "data_obj_ref",
           parameter "nonlocal_genome_names" of list of type "data_obj_name",
           parameter "input_genomeset_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type
           "KButil_Remove_Genomes_from_GenomeSet_Output" -> structure:
           parameter "report_name" of type "data_obj_name", parameter
           "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Remove_Genomes_from_GenomeSet

        # init
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Remove_Genomes_from_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple


        # check params
        required_params = ['workspace_name',
                           'input_genomeset_ref',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Reduced GenomeSet'
        if not params.get('input_genome_refs') and \
           not params.get('nonlocal_genome_names'):
            raise ValueError('must define either Local genomes or Non-local genomes to remove')

            
        # read orig GenomeSet
        #
        genomeSet_workspace = None
        if 'input_genomeset_ref' in params and params['input_genomeset_ref'] is not None:

            (genomeSet,
             info,
             obj_name,
             type_name) = self.get_obj_data(params['input_genomeset_ref'], 'genomeSet')

            if type_name != 'GenomeSet':
                raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")
            genomeSet_workspace = info[WORKSPACE_I]


        # Build list of genome refs (without version) to skip.
        #  Note: standardize to workspace_name and obj_id
        skip_genomes_by_ref = dict()
        nonlocal_skip_genome_refs = []
        if params.get('input_genome_refs'):
            for genomeRef in params['input_genome_refs']: 
                (this_obj_info,
                 this_obj_name,
                 this_obj_type) = self.get_obj_info(genomeRef, 'genome')

                standardized_genomeRef = self.get_obj_ref_from_obj_info_noVer(this_obj_info)
                skip_genomes_by_ref[standardized_genomeRef] = True
        if params.get('nonlocal_genome_names'):
            for gId in list(genomeSet['elements'].keys()):
                genomeRef = genomeSet['elements'][gId]['ref']
                (genome_obj_info,
                 this_genome_objname,
                 type_name) = self.get_obj_info(genomeRef, 'genome')

                this_genome_workspace = genome_obj_info[WORKSPACE_I]
                standardized_genomeRef = self.get_obj_ref_from_obj_info_noVer(genome_obj_info)
                if this_genome_workspace != genomeSet_workspace \
                   and this_genome_objname in params['nonlocal_genome_names']:
                    skip_genomes_by_ref[standardized_genomeRef] = True
                    nonlocal_skip_genome_refs.append(standardized_genomeRef)
                
        # build new genome set without skip genomes
        elements = dict()
        for gId in list(genomeSet['elements'].keys()):
            genomeRef = genomeSet['elements'][gId]['ref']
            (this_obj_info,
             this_genome_obj_name,
             this_genome_obj_type) = self.get_obj_info(genomeRef, 'genome')

            standardized_genomeRef = self.get_obj_ref_from_obj_info_noVer(this_obj_info)

            # this is where they are removed
            if not skip_genomes_by_ref.get(standardized_genomeRef):
                elements[gId] = dict()
                elements[gId]['ref'] = genomeRef  # the key line
                self.log(console, "keeping element " + gId + " : " + genomeRef)
            else:
                self.log(console, "removing element " + gId + " : " + genomeRef)

        # set provenance
        self.log(console, "SETTING PROVENANCE")
        input_ws_obj_refs = [params['input_genomeset_ref']]
        input_ws_obj_refs.extend(params['input_genome_refs'])
        provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Remove_Genomes_from_GenomeSet')

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                       'objects': [{
                                                           'type': 'KBaseSearch.GenomeSet',
                                                           'data': output_GenomeSet,
                                                           'name': params['output_name'],
                                                           'meta': {},
                                                           'provenance': provenance}]})[0]

        # build output report object
        self.log(console, "BUILDING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                     str(len(list(elements.keys()))))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(list(elements.keys()))) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Remove_Genomes_from_GenomeSet'}],
                'text_message': report}
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Remove_Genomes_from_GenomeSet DONE")
        #END KButil_Remove_Genomes_from_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Remove_Genomes_from_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Build_ReadsSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Build_ReadsSet_Params"
           (KButil_Build_ReadsSet() ** **  Method for creating a ReadsSet) ->
           structure: parameter "workspace_name" of type "workspace_name" (**
           The workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Build_ReadsSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Build_ReadsSet
        console = []
        invalid_msgs = []
        self.log(console,'Running KButil_Build_ReadsSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Built ReadsSet'

            
        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 1:
            self.log(console,"Must provide at least one Reads Lib")
            self.log(invalid_msgs,"Must provide at least one Reads Lib")

        # Build ReadsSet
        #
        items = []
        lib_seen = dict()
        set_type = None

        for libRef in params['input_refs']:

            if not lib_seen.get(libRef):
                lib_seen[libRef] = True

                (libObj,
                 info,
                 lib_name,
                 lib_type) = self.get_obj_data(libRef, 'reads library')

                if set_type is None:
                    set_type = lib_type
                elif lib_type != set_type:
                    raise ValueError("Don't currently support heterogeneous ReadsSets"+
                                     " (e.g. PairedEndLibrary and SingleEndLibrary)." +
                                     " You have more than one type in your input")

                if lib_type != 'SingleEndLibrary' and lib_type != 'PairedEndLibrary':
                    errMsg = "Bad Type: Should be SingleEndLibrary or PairedEndLibrary instead of "
                    errMsg += "'{}' for ref: '{}'"
                    raise ValueError(errMsg.format(lib_type, libRef))

                # add lib
                self.log(console, "adding lib " + lib_name + " : " + libRef)
                items.append({'ref': libRef, 'label': lib_name})


        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING READS_SET")

            output_readsSet_obj = {'description': params['desc'],
                                   'items': items}
            output_readsSet_name = params['output_name']
            try:
                rSet_ref = self.setAPI_Client.save_reads_set_v1(
                    {'workspace_name': params['workspace_name'],
                     'output_object_name': output_readsSet_name,
                     'data': output_readsSet_obj})['set_ref']
            except Exception as e:
                errMsg = 'SetAPI Error: Unable to save read library set obj to workspace: ({})\n{}'
                raise ValueError(errMsg.format(params['workspace_name'], str(e)))

        # build output report object
        #
        self.log(console, "SAVING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console, "reads libs in output set " + params['output_name'] + ": " +
                     str(len(params['input_refs'])))
            report += 'reads libs in output set ' + params['output_name'] + ': ' + str(
                len(params['input_refs']))
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                    'description': 'KButil_Build_ReadsSet'}],
                'text_message': report}
        else:
            report += "FAILURE:\n\n"+"\n".join(invalid_msgs)+"\n"
            reportObj = {'objects_created': [], 'text_message': report}

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console, "KButil_Build_ReadsSet DONE")
        #END KButil_Build_ReadsSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Build_ReadsSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Merge_MultipleReadsSets_to_OneReadsSet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Merge_MultipleReadsSets_to_OneReadsSet_Params"
           (KButil_Merge_MultipleReadsSets_to_OneReadsSet() ** **  Method for
           merging multiple ReadsSets into one ReadsSet) -> structure:
           parameter "workspace_name" of type "workspace_name" (** The
           workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type
           "KButil_Merge_MultipleReadsSets_to_OneReadsSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Merge_MultipleReadsSets_to_OneReadsSet
        console = []
        report = ''
        self.log(console, 'Running KButil_Merge_MultipleReadsSets_to_OneReadsSet with parameters: ')
        self.log(console, "\n"+pformat(params))

        # check params
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 2:
            self.log(console,"Must provide at least two ReadsSets")
            self.log(invalid_msgs,"Must provide at least two ReadsSets")

        # init output object fields and SetAPI
        combined_readsSet_ref_list   = []
        combined_readsSet_name_list  = []
        combined_readsSet_label_list = []

        # Iterate through list of ReadsSets
        #
        reads_lib_type = None
        reads_lib_ref_seen = dict()
        accepted_libs = []
        repeat_libs = []
        for set_i,this_readsSet_ref in enumerate(params['input_refs']):
            accepted_libs.append([])
            repeat_libs.append([])

            (input_reads_obj_info,
             input_reads_obj_name,
             input_reads_obj_type) = self.get_obj_info(this_readsSet_ref, 'reads set', full_type=True)
            
            acceptable_types = ["KBaseSets.ReadsSet"]
            if input_reads_obj_type not in acceptable_types:
                raise ValueError("Input reads of type: '" + input_reads_obj_type +
                                 "'.  Must be one of " + ", ".join(acceptable_types))

            # iterate through read libraries in read set and add new ones to combined ReadsSet
            try:
                input_readsSet_obj = self.setAPI_Client.get_reads_set_v1({
                    'ref': this_readsSet_ref,
                    'include_item_info': 1})
            except Exception as e:
                raise ValueError('SetAPI Error: Unable to get read library set from workspace: (' +
                                 this_readsSet_ref + ")\n" + str(e))

            for readsLibrary_obj in input_readsSet_obj['data']['items']:
                this_readsLib_ref    = readsLibrary_obj['ref']
                this_readsLib_label  = readsLibrary_obj['label']
                (this_readsLib_name, this_readsLib_type) = self.get_obj_name_and_type_from_obj_info (readsLibrary_obj['info'])
                if reads_lib_type is None:
                    reads_lib_type = this_readsLib_type
                elif this_readsLib_type != reads_lib_type:
                    raise ValueError ("inconsistent reads library types in ReadsSets.  " +
                                      "Must all be PairedEndLibrary or SingleEndLibrary to merge")

                if this_readsLib_ref not in reads_lib_ref_seen:
                    reads_lib_ref_seen[this_readsLib_ref] = True
                    combined_readsSet_ref_list.append(this_readsLib_ref)
                    combined_readsSet_label_list.append(this_readsLib_label)
                    combined_readsSet_name_list.append(this_readsLib_name)
                    accepted_libs[set_i].append(this_readsLib_ref)
                else:
                    repeat_libs[set_i].append(this_readsLib_ref)

        # Save Merged ReadsSet
        #
        items = []
        for lib_i,lib_ref in enumerate(combined_readsSet_ref_list):
            items.append({'ref': lib_ref,
                          'label': combined_readsSet_label_list[lib_i]
                          #'data_attachment': ,
                          #'info':
                              })
        output_readsSet_obj = { 'description': params['desc'],
                                'items': items
                              }
        output_readsSet_name = params['output_name']
        try:
            output_readsSet_ref = self.setAPI_Client.save_reads_set_v1 ({'workspace_name': params['workspace_name'],
                                                                    'output_object_name': output_readsSet_name,
                                                                    'data': output_readsSet_obj
                                                                    })['set_ref']
        except Exception as e:
            raise ValueError('SetAPI FAILURE: Unable to save read library set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        # build report
        #
        self.log (console, "SAVING REPORT")
        report += "TOTAL READS LIBRARIES COMBINED INTO ONE READS SET: "+ str(len(combined_readsSet_ref_list))+"\n"
        for set_i,this_readsLib_ref in enumerate(params['input_refs']):
            report += "READS LIBRARIES ACCEPTED FROM ReadsSet "+str(set_i)+": "+str(len(accepted_libs[set_i]))+"\n"
            report += "READS LIBRARIES REPEAT FROM ReadsSet "+str(set_i)+":   "+str(len(repeat_libs[set_i]))+"\n"
            report += "\n"
        reportObj = {'objects_created':[],
                     'text_message': report}

        reportObj['objects_created'].append({'ref':output_readsSet_ref,
                                             'description':params['desc']})


        # save report object
        #
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console,"KButil_Merge_MultipleReadsSets_to_OneReadsSet DONE")
        #END KButil_Merge_MultipleReadsSets_to_OneReadsSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Merge_MultipleReadsSets_to_OneReadsSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Build_AssemblySet(self, ctx, params):
        """
        :param params: instance of type "KButil_Build_AssemblySet_Params"
           (KButil_Build_AssemblySet() ** **  Method for creating an
           AssemblySet) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** ** 
           objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_refs" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Build_AssemblySet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Build_AssemblySet
        console = []
        invalid_msgs = []
        self.log(console,'Running KButil_Build_AssemblySet with params=')
        self.log(console, "\n"+pformat(params))
        report = ''


        # check params
        required_params = ['workspace_name',
                           'input_refs',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Built AssemblySet'

            
        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 1:
            self.log(console,"Must provide at least one Assembly")
            self.log(invalid_msgs,"Must provide at least one Assembly")


        # Build AssemblySet
        #
        items = []
        ass_seen = dict()
        set_type = None

        for assRef in params['input_refs']:

            if not ass_seen.get(assRef):
                ass_seen[assRef] = True

                (assObj,
                 info,
                 ass_name,
                 ass_type) = self.get_obj_data(assRef, 'assembly')

                if set_type != None:
                    if ass_type != set_type:
                        raise ValueError ("Don't currently support heterogeneous AssemblySets.  You have more than one type in your input")
                    set_type = ass_type

                # add assembly
                self.log(console,"adding assembly "+ass_name+" : "+assRef)
                items.append ({'ref': assRef,
                               'label': ass_name
                               #'data_attachment': ,
                               #'info'
                               })


        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING ASSEMBLY_SET")
            output_assemblySet_obj = { 'description': params['desc'],
                                       'items': items
                                     }
            output_assemblySet_name = params['output_name']
            try:
                output_assemblySet_ref = self.setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                        'output_object_name': output_assemblySet_name,
                                                                        'data': output_assemblySet_obj
                                                                        })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        # build output report object
        #
        self.log(console,"SAVING REPORT")
        if len(invalid_msgs) == 0:
            self.log(console,"assembly objs in output set "+params['output_name']+": "+str(len(params['input_refs'])))
            report += 'assembly objs in output set '+params['output_name']+': '+str(len(params['input_refs']))
            reportObj = {
                'objects_created':[{'ref':params['workspace_name']+'/'+params['output_name'], 'description':'KButil_Build_AssemblySet'}],
                'text_message':report
                }
        else:
            report += "FAILURE:\n\n"+"\n".join(invalid_msgs)+"\n"
            reportObj = {
                'objects_created':[],
                'text_message':report
                }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console,"KButil_Build_AssemblySet DONE")
        #END KButil_Build_AssemblySet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Build_AssemblySet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Batch_Create_ReadsSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Batch_Create_ReadsSet_Params"
           (KButil_Batch_Create_ReadsSet() ** **  Method for creating a
           ReadsSet without specifying individual objects) -> structure:
           parameter "workspace_name" of type "workspace_name" (** The
           workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "name_pattern" of String, parameter "output_name" of
           type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Batch_Create_ReadsSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Batch_Create_ReadsSet

        #### STEP 0: standard method init
        ##
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console,'Running KButil_Batch_Create_ReadsSet with params=')
        self.log(console, "\n"+pformat(params))
        report = ''

        
        # check params
        required_params = ['workspace_name',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Batch Created ReadsSet'


        #### STEP 3: refine name_pattern
        ##
        name_pattern = params.get('name_pattern')
        if name_pattern:
            name_pattern = name_pattern.strip()
            name_pattern = name_pattern.strip('*')
            name_pattern = name_pattern.replace('.','\.')
            name_pattern = name_pattern.replace('*','.*')

            regexp_name_pattern = re.compile ('^.*'+name_pattern+'.*$')


        #### STEP 4: read ws for readslib objects
        ##
        pe_reads_obj_ref_by_name = dict()
        se_reads_obj_ref_by_name = dict()
        reads_obj_ref_by_name    = None

        # Paired End
        pe_reads_obj_info_list = self.get_obj_info_list_from_ws_name(params['workspace_name'],
                                                                     'KBaseFile.PairedEndLibrary',
                                                                     'Paired-End Reads Library')
        for info in pe_reads_obj_info_list:
            reads_ref = self.get_obj_ref_from_obj_info(info)
            (reads_name, type_name) = self.get_obj_name_and_type_from_obj_info (info)

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' READS_NAME: '"+reads_name+"'")

            if not name_pattern or regexp_name_pattern.match(reads_name):
                self.log(console, "ADDING "+reads_name+" ("+reads_ref+")")
                pe_reads_obj_ref_by_name[reads_name] = reads_ref

        # Single End
        se_reads_obj_info_list = self.get_obj_info_list_from_ws_name(params['workspace_name'],
                                                                     'KBaseFile.SingleEndLibrary',
                                                                     'Single-End Reads Library')
        for info in se_reads_obj_info_list:
            reads_ref = self.get_obj_ref_from_obj_info(info)
            (reads_name, type_name) = self.get_obj_name_and_type_from_obj_info (info)

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' READS_NAME: '"+reads_name+"'")

            if not name_pattern or regexp_name_pattern.match(reads_name):
                self.log(console, "ADDING "+reads_name+" ("+reads_ref+")")
                se_reads_obj_ref_by_name[reads_name] = reads_ref

        # check for no hits
        if len(list(pe_reads_obj_ref_by_name.keys())) == 0 \
           and len(list(se_reads_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Reads Library objects found")
            else:
                self.log(invalid_msgs, "No Reads Library objects passing name_pattern filter: '"+name_pattern+"'")

                
        #### STEP 5: Build ReadsSet
        ##
        if len(invalid_msgs) == 0:
            items = []
            reads_ref_list = []

            # pick whether to use single end or paired end hits (favor paired end)
            if len(list(pe_reads_obj_ref_by_name.keys())) == 0 \
               and len(list(se_reads_obj_ref_by_name.keys())) != 0:
                reads_obj_ref_by_name = se_reads_obj_ref_by_name
            else:
                reads_obj_ref_by_name = pe_reads_obj_ref_by_name

            # add readslibs
            for reads_name in sorted (reads_obj_ref_by_name.keys()):
                reads_ref = reads_obj_ref_by_name[reads_name]
                reads_ref_list.append (reads_ref)

                self.log(console,"adding reads library "+reads_name+" : "+reads_ref)
                items.append ({'ref': reads_ref,
                               'label': reads_name
                               #'data_attachment': ,
                               #'info'
                           })


        #### STEP 6: Store output object
        ##
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING READS_SET")

            # object def
            output_readsSet_obj = { 'description': params['desc'],
                                    'items': items
                                }
            output_readsSet_name = params['output_name']
            # object save
            try:
                output_readsSet_ref = self.setAPI_Client.save_reads_set_v1 ({'workspace_name': params['workspace_name'],
                                                                              'output_object_name': output_readsSet_name,
                                                                              'data': output_readsSet_obj
                                                                          })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save reads library set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        #### STEP 7: build output report object
        ##
        self.log(console,"SAVING REPORT")
        if len(invalid_msgs) != 0:
            report += "\n".join(invalid_msgs)
            reportObj = {
                'objects_created':[],
                'text_message':report
            }
        else:
            self.log(console,"reads library objs in output set "+params['output_name']+": "+str(len(items)))
            report += 'reads library objs in output set '+params['output_name']+': '+str(len(items))
            desc = 'KButil_Batch_Create_ReadsSet'
            if name_pattern:
                desc += ' with name_pattern: '+name_pattern
            reportObj = {
                'objects_created':[{'ref':params['workspace_name']+'/'+params['output_name'], 'description':desc}],
                'text_message':report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console,"KButil_Batch_Create_ReadsSet DONE")
        #END KButil_Batch_Create_ReadsSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Batch_Create_ReadsSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Batch_Create_AssemblySet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Batch_Create_AssemblySet_Params"
           (KButil_Batch_Create_AssemblySet() ** **  Method for creating an
           AssemblySet without specifying individual objects) -> structure:
           parameter "workspace_name" of type "workspace_name" (** The
           workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "name_pattern" of String, parameter "output_name" of
           type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Batch_Create_AssemblySet_Output"
           -> structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Batch_Create_AssemblySet

        #### STEP 0: standard method init
        ##
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console,'Running KButil_Batch_Create_AssemblySet with params=')
        self.log(console, "\n"+pformat(params))
        report = ''

        
        # check params
        required_params = ['workspace_name',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Batch Created AssemblySet'


        #### STEP 3: refine name_pattern
        ##
        name_pattern = params.get('name_pattern')
        if name_pattern:
            name_pattern = name_pattern.strip()
            name_pattern = name_pattern.strip('*')
            name_pattern = name_pattern.replace('.','\.')
            name_pattern = name_pattern.replace('*','.*')

            regexp_name_pattern = re.compile ('^.*'+name_pattern+'.*$')


        #### STEP 4: read ws for assembly objects
        ##
        assembly_obj_ref_by_name = dict()
        assembly_obj_info_list = self.get_obj_info_list_from_ws_name(params['workspace_name'],
                                                                     'KBaseGenomeAnnotations.Assembly',
                                                                     'Assembly')
        for info in assembly_obj_info_list:
            assembly_ref = self.get_obj_ref_from_obj_info(info)
            (assembly_name, type_name) = self.get_obj_name_and_type_from_obj_info (info)

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' ASSEMBLY_NAME: '"+assembly_name+"'")

            if not name_pattern or regexp_name_pattern.match(assembly_name):
                self.log(console, "ADDING "+assembly_name+" ("+assembly_ref+")")
                assembly_obj_ref_by_name[assembly_name] = assembly_ref

        if len(list(assembly_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Assembly objects found")
            else:
                self.log(invalid_msgs, "No Assembly objects passing name_pattern filter: '"+name_pattern+"'")


        #### STEP 5: Build AssemblySet
        ##
        if len(invalid_msgs) == 0:
            items = []
            assembly_ref_list = []
            for ass_name in sorted (assembly_obj_ref_by_name.keys()):
                # add assembly
                ass_ref = assembly_obj_ref_by_name[ass_name]
                assembly_ref_list.append (ass_ref)

                self.log(console,"adding assembly "+ass_name+" : "+ass_ref)
                items.append ({'ref': ass_ref,
                               'label': ass_name
                               #'data_attachment': ,
                               #'info'
                           })


        #### STEP 6: Store output object
        ##
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING ASSEMBLY_SET")

            # object def
            output_assemblySet_obj = { 'description': params['desc'],
                                       'items': items
                                   }
            output_assemblySet_name = params['output_name']
            # object save
            try:
                output_assemblySet_ref = self.setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                              'output_object_name': output_assemblySet_name,
                                                                              'data': output_assemblySet_obj
                                                                          })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        #### STEP 7: build output report object
        ##
        self.log(console,"SAVING REPORT")
        if len(invalid_msgs) != 0:
            report += "\n".join(invalid_msgs)
            reportObj = {
                'objects_created':[],
                'text_message':report
            }
        else:
            self.log(console,"assembly objs in output set "+params['output_name']+": "+str(len(items)))
            report += 'assembly objs in output set '+params['output_name']+': '+str(len(items))
            desc = 'KButil_Batch_Create_AssemblySet'
            if name_pattern:
                desc += ' with name_pattern: '+name_pattern
            reportObj = {
                'objects_created':[{'ref':params['workspace_name']+'/'+params['output_name'], 'description':desc}],
                'text_message':report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console,"KButil_Batch_Create_AssemblySet DONE")
        #END KButil_Batch_Create_AssemblySet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Batch_Create_AssemblySet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Batch_Create_GenomeSet(self, ctx, params):
        """
        :param params: instance of type
           "KButil_Batch_Create_GenomeSet_Params"
           (KButil_Batch_Create_GenomeSet() ** **  Method for creating a
           GenomeSet without specifying individual objects) -> structure:
           parameter "workspace_name" of type "workspace_name" (** The
           workspace object refs are of form: ** **    objects =
           ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "name_pattern" of String, parameter "output_name" of
           type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Batch_Create_GenomeSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Batch_Create_GenomeSet

        #### STEP 0: standard method init
        ##
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console,'Running KButil_Batch_Create_GenomeSet with params=')
        self.log(console, "\n"+pformat(params))
        report = ''
        

        # check params
        required_params = ['workspace_name',
                           'output_name'
                           ]
        self.check_params (params, required_params)
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Batch Created GenomeSet'


        #### STEP 3: refine name_pattern
        ##
        name_pattern = params.get('name_pattern')
        if name_pattern:
            name_pattern = name_pattern.strip()
            name_pattern = name_pattern.strip('*')
            name_pattern = name_pattern.replace('.','\.')
            name_pattern = name_pattern.replace('*','.*')

            regexp_name_pattern = re.compile ('^.*'+name_pattern+'.*$')


        #### STEP 4: read ws for genome objects
        ##
        genome_obj_ref_by_name = dict()
        genome_obj_info_list = self.get_obj_info_list_from_ws_name(params['workspace_name'],
                                                                   'KBaseGenomes.Genome',
                                                                   'Genome')
        for info in genome_obj_info_list:
            genome_ref = self.get_obj_ref_from_obj_info(info)
            (genome_name, type_name) = self.get_obj_name_and_type_from_obj_info (info)

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' GENOME_NAME: '"+genome_name+"'")

            if not name_pattern or regexp_name_pattern.match(genome_name):
                self.log(console, "ADDING "+genome_name+" ("+genome_ref+")")
                genome_obj_ref_by_name[genome_name] = genome_ref

        if len(list(genome_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Genome objects found")
            else:
                self.log(invalid_msgs, "No Genome objects passing name_pattern filter: '"+name_pattern+"'")

                
        #### STEP 5: Build GenomeSet
        ##
        if len(invalid_msgs) == 0:
            #items = []
            elements = dict()
            genome_ref_list = []
            for gen_name in sorted (genome_obj_ref_by_name.keys()):
                # add genome
                gen_ref = genome_obj_ref_by_name[gen_name]
                genome_ref_list.append (gen_ref)

                self.log(console,"adding genome "+gen_name+" : "+gen_ref)
                #items.append ({'ref': gen_ref,
                #               'label': gen_name
                #               #'data_attachment': ,
                #               #'info'
                #           })
                elements[gen_name] = dict()
                elements[gen_name]['ref'] = gen_ref


        #### STEP 6: Store output object
        ##
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING GENOME_SET")

            # set provenance
            self.log(console, "SETTING PROVENANCE")
            input_ws_obj_refs = genome_ref_list
            provenance = self.set_provenance(ctx, input_ws_obj_refs, 'kb_SetUtilities', 'KButil_Batch_Create_GenomeSet')

            # object def
            output_genomeSet_obj = { 'description': params['desc'],
                                     #'items': items
                                     'elements': elements
                                   }
            output_genomeSet_name = params['output_name']
            # object save
            try:
                new_obj_info = self.wsClient.save_objects({'workspace': params['workspace_name'],
                                                      'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                                   'data': output_genomeSet_obj,
                                                                   'name': output_genomeSet_name,
                                                                   'meta': {},
                                                                   'provenance': provenance
                                                               }]
                                                  })[0]
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save genome set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        #### STEP 7: build output report object
        ##
        self.log(console,"SAVING REPORT")
        if len(invalid_msgs) != 0:
            report += "\n".join(invalid_msgs)
            reportObj = {
                'objects_created':[],
                'text_message':report
            }
        else:
            self.log(console,"genome objs in output set "+params['output_name']+": "+str(len(list(elements.keys()))))
            report += 'genome objs in output set '+params['output_name']+': '+str(len(list(elements.keys())))
            desc = 'KButil_Batch_Create_GenomeSet'
            if name_pattern:
                desc += ' with name_pattern: '+name_pattern
            reportObj = {
                'objects_created':[{'ref':params['workspace_name']+'/'+params['output_name'], 'description':desc}],
                'text_message':report
            }

        # Save report
        report_info = self.reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
        self.log(console,"KButil_Batch_Create_GenomeSet DONE")
        #END KButil_Batch_Create_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Batch_Create_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def KButil_Summarize_GenomeSet(self, ctx, params):
        """
        :param params: instance of type "KButil_Summarize_GenomeSet_Params"
           (KButil_Summarize_GenomeSet() ** **  Method for building an HTML
           report with Genome summaries) -> structure: parameter
           "workspace_name" of type "workspace_name" (** The workspace object
           refs are of form: ** **    objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_ref" of type "data_obj_ref", parameter
           "use_newest_version" of type "bool", parameter "show_sci_name" of
           type "bool", parameter "add_qc" of type "bool", parameter
           "add_env_bioelement" of type "bool", parameter "add_dbCAN" of type
           "bool", parameter "checkM_reduced_tree" of type "bool"
        :returns: instance of type "KButil_Summarize_GenomeSet_Output" ->
           structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Summarize_GenomeSet
        console = []
        invalid_msgs = []
        self.log(console, 'Running Summarize_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        outdir = os.path.join(self.outdir, 'summarize_genomeset')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        html_dir = os.path.join(outdir, 'html')
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        logMsg = ''
        report = ''

        #### check params
        ##
        required_params = ['workspace_name',
                           'input_ref',
                           'use_newest_version',
                           'show_sci_name',
                           'add_qc',
                           'add_env_bioelement',
                           'add_dbCAN'
        ]
        self.check_params (params, required_params)

        #### default params
        ##
        default_params = { 'checkM_reduced_tree': 1 }
        for param in default_params.keys():
            if param not in params:
                params[param] = default_params[param]
                

        #### Get GenomeSet
        ##
        GenomeSet_element_refs = dict()
        (genomeSet_data,
         info,
         genomeSet_obj_name,
         type_name) = self.get_obj_data(params['input_ref'], 'genomeSet')

        if type_name != 'GenomeSet':
            raise ValueError("Bad Type:  Should be GenomeSet instead of '" + type_name + "'")

        genome_newVer_ref_to_oldVer_ref = dict()
        genome_newVer_ref_to_obj_name = dict()
        genome_obj_name_to_newVer_ref = dict()
        genome_newVer_ref_order = []
        for genome_id in sorted(genomeSet_data['elements'].keys()):
            genome_oldVer_ref = genomeSet_data['elements'][genome_id]['ref']

            (genome_obj_info,
             genome_obj_name,
             genome_obj_type) = self.get_newest_obj_info (genome_oldVer_ref, 'genome', full_type=True)

            #acceptable_types = ["KBaseGenomes.Genome","KBaseGenomeAnnotations.GenomeAnnotation"]
            acceptable_types = ["KBaseGenomes.Genome"]
            if genome_obj_type not in acceptable_types:
                raise ValueError("Input Genome of type: '" + genome_obj_type +
                                 "'.  Must be one of " + ", ".join(acceptable_types))
            # get newVer ref
            genome_newVer_ref = self.get_obj_ref_from_obj_info (genome_obj_info)

            # store mappings
            genome_newVer_ref_to_oldVer_ref[genome_newVer_ref] = genome_oldVer_ref
            genome_newVer_ref_to_obj_name[genome_newVer_ref]   = genome_obj_name
            
            # can have same obj_name in different workspaces, so must be a list of refs
            if 'genome_obj_name' not in genome_obj_name_to_newVer_ref:
                genome_obj_name_to_newVer_ref[genome_obj_name] = []
            genome_obj_name_to_newVer_ref[genome_obj_name].append(genome_newVer_ref)


        # sort refs by genome name
        for genome_obj_name in sorted(genome_obj_name_to_newVer_ref.keys()):
            for genome_newVer_ref in genome_obj_name_to_newVer_ref[genome_obj_name]:
                genome_newVer_ref_order.append(genome_newVer_ref)


        #### populate table info
        ##
        table = dict()

        # QC
        if int(params.get('add_qc', 0)) == 1:
            for genome_newVer_ref in genome_newVer_ref_order:

                if genome_newVer_ref not in table:
                    table[genome_newVer_ref] = dict()

                # want to obtain QC from newest object if it's been stored in Genome
                (genome_data,
                 info,
                 this_genome_obj_name,
                 type_name) = self.get_obj_data(genome_newVer_ref, 'genome')

                # preferrably read QC from Genome object
                if len(genome_data.get('quality_scores',[])) > 0:
                    for qual_score in genome_data['quality_scorres']:
                        if 'method' in qual_score and 'score' in qual_score:
                            if qual_score['method'] == 'CheckM_completeness':
                                table[genome_newVer_ref]['qc_complete'] = qual_score['score']
                            elif qual_score['method'] == 'CheckM_contamination':
                                table[genome_newVer_ref]['qc_contam'] = qual_score['score']

            # run CheckM as subprocess for any Genomes that are missing QC scores
            missing_qc = False
            for genome_newVer_ref in genome_newVer_ref_order:
                if 'qc_complete' not in table[genome_newVer_ref] or \
                   'qc_contam' not in table[genome_newVer_ref]:
                    
                    missing_qc = True

            if missing_qc:
                sub_method = 'CheckM'
                checkM_params = {'workspace_name': params['workspace_name'],
                                 'input_ref': params['input_ref'],
                                 'reduced_tree': params['checkM_reduced_tree'],
                                 'save_output_dir': '0',
                                 'save_plots_dir': '0',
                                 'threads': 4
                                 }
                self.log(console, 'RUNNING CheckM')
                try:
                    checkM_Client = kb_Msuite(self.callbackURL, token=self.token, service_ver=self.SERVICE_VER)
                except Exception as e:
                    raise ValueError("unable to instantiate checkM_Client. "+str(e))
                try:
                    this_retVal = checkM_Client.run_checkM_lineage_wf(checkM_params)
                except Exception as e:
                    raise ValueError ("unable to run "+sub_method+". "+str(e))
                try:
                    this_report_obj = self.wsClient.get_objects2({'objects':[{'ref':this_retVal['report_ref']}]})['data'][0]['data']
                except Exception as e:
                    raise ValueError("unable to fetch "+sub_method+" report: " + this_retVal['report_ref']+". "+str(e))

                # retrieve CheckM TSV file
                checkM_outdir = os.path.join(outdir, 'checkM')
                if not os.path.exists(checkM_outdir):
                    os.makedirs(checkM_outdir)
                checkM_tsv_outfile = os.path.join(checkM_outdir, 'checkM_summary.tsv')
                found_checkM_summary = False
                if len(this_report_obj.get('file_links',[])) > 0:
                    for file_link in this_report_obj['file_links']:
                        if 'name' in file_link and file_link['name'] == 'CheckM_summary_table.tsv.zip':
                            self.log(console, "CheckM FILE_LINK contents")
                            for key in file_link.keys():
                                self.log(console, "FILE_LINK "+key+": "+file_link[key])
                                
                            download_ret = self.dfuClient.shock_to_file({'handle_id': file_link['handle'],
                                                                         'file_path': checkM_tsv_outfile+'.zip',
#                                                                         'file_path': checkM_tsv_outfile,
#                                                                         'file_path': checkM_outdir,
                                                                         'unpack': 'unpack'})
                            for key in download_ret.keys():
                                self.log(console, "DOWNLOAD "+str(key)+": "+str(download_ret[key]))
                            #checkM_tsv_path = download_ret['file_path']
                            #checkM_tsv_path= download_ret['file_path'].replace('.zip','')
                            checkM_tsv_outfile= download_ret['node_file_name'].replace('.zip','')
                            found_checkM_summary = True
                            break
                if not found_checkM_summary:
                    raise ValueError ("Failure retrieving CheckM summary TSV file")
                [GENOME_I, LINEAGE_I, GENOME_CNT_I, MARKER_CNT_I, MARKER_SET_I, CNT_0, CNT_1, CNT_2, CNT_3, CNT_4, CNT_5plus, COMPLETENESS_I, CONTAMINATION_I] = range(13)
                self.log(console, "CheckM TSV:")
                checkM_tsv_path = os.path.join(checkM_outdir, checkM_tsv_outfile)
                with open (checkM_tsv_path, 'r') as checkM_tsv_handle:
                    for checkM_line in checkM_tsv_handle.readlines():
                        checkM_line = checkM_line.rstrip()
                        self.log(console, checkM_line)
                        checkM_info = checkM_line.split("\t")
                        genome_name = checkM_info[GENOME_I]
                        if genome_name == 'Bin Name':
                            continue
                        for genome_newVer_ref in genome_obj_name_to_newVer_ref[genome_name]:
                            table[genome_newVer_ref]['qc_complete'] = checkM_info[COMPLETENESS_I]
                            table[genome_newVer_ref]['qc_contam'] = checkM_info[CONTAMINATION_I]

                            
        #### read genome objects to get rest of table info
        ##
        for genome_newVer_ref in genome_newVer_ref_order:

            if genome_newVer_ref not in table:
                table[genome_newVer_ref] = dict()
                
            if int(params['use_newest_version']) == 0:
                genome_ref = genome_newVer_ref_to_oldVer_ref[genome_newVer_ref]
            else:
                genome_ref = genome_newVer_ref
                
            (genome_data,
             info,
             this_genome_obj_name,
             type_name) = self.get_obj_data(genome_ref, 'genome')
            
            if int(params.get('show_sci_name',1)) == 1:
                table[genome_newVer_ref]['sci_name'] = self.get_genome_attribute(genome_data, 'sci_name', genome_newVer_ref)
            table[genome_newVer_ref]['taxonomy'] = self.get_genome_attribute(genome_data, 'taxonomy', genome_newVer_ref)
            table[genome_newVer_ref]['contig_count'] = self.get_genome_attribute(genome_data, 'contig_count', genome_newVer_ref)
            table[genome_newVer_ref]['genome_length'] = self.get_genome_attribute(genome_data, 'genome_length', genome_newVer_ref)
            table[genome_newVer_ref]['N50'] = self.get_genome_attribute(genome_data, 'N50', genome_newVer_ref)
            table[genome_newVer_ref]['GC'] = self.get_genome_attribute(genome_data, 'GC', genome_newVer_ref)
            table[genome_newVer_ref]['CDS_count'] = self.get_genome_attribute(genome_data, 'CDS_count', genome_newVer_ref)
            table[genome_newVer_ref]['tRNA_count'] = self.get_genome_attribute(genome_data, 'tRNA_count', genome_newVer_ref)
            table[genome_newVer_ref]['5S_rRNA_count'] = self.get_genome_attribute(genome_data, '5S_rRNA_count', genome_newVer_ref)
            table[genome_newVer_ref]['16S_rRNA_count'] = self.get_genome_attribute(genome_data, '16S_rRNA_count', genome_newVer_ref)
            table[genome_newVer_ref]['23S_rRNA_count'] = self.get_genome_attribute(genome_data, '23S_rRNA_count', genome_newVer_ref)
            table[genome_newVer_ref]['CRISPR_array_count'] = self.get_genome_attribute(genome_data, 'CRISPR_array_count', genome_newVer_ref)


        #### build TSV table
        ##
        TSV_table_buf = []
        field_titles = {'sci_name': 'Scientific Name',
                        'taxonomy': 'Taxonomy',
                        'qc_complete': 'CheckM Complete',
                        'qc_contam': 'CheckM Contam',
                        'contig_count': 'Num Contigs',
                        'genome_length': 'Genome Size (bp)',
                        'N50': 'N50',
                        'GC': 'G+C%',
                        'CDS_count': 'CDS',
                        'tRNA_count': 'tRNA',
                        '5S_rRNA_count': '5S rRNA',
                        '16S_rRNA_count': '16S rRNA',
                        '23S_rRNA_count': '23S rRNA',
                        'CRISPR_array_count': 'CRISPR arrays'}
        fields = []
        if int(params.get('show_sci_name',1)) == 1:
            fields.append('sci_name')
        fields.append('taxonomy')
        if int(params.get('add_qc', 0)) == 1:
            fields.extend(['qc_complete', 'qc_contam'])
        fields.extend(['contig_count',
                       'genome_length',
                       'N50',
                       'GC',
                       'CDS_count',
                       'tRNA_count',
                       '5S_rRNA_count',
                       '16S_rRNA_count',
                       '23S_rRNA_count',
                       'CRISPR_array_count'])
        # header
        TSV_row = ['Genome']
        for field in fields:
            TSV_row.append(field_titles[field])
        TSV_table_buf.append("\t".join(TSV_row))

        # data
        for genome_newVer_ref in genome_newVer_ref_order:
            genome_obj_name = genome_newVer_ref_to_obj_name[genome_newVer_ref]
            TSV_row = [genome_obj_name]
            for field in fields:
                TSV_row.append(table[genome_newVer_ref][field])
            TSV_table_buf.append("\t".join(TSV_row))

        # report in log
        for row in TSV_table_buf:
            self.log(console, row)

        # write TSV to file and upload
        TSV_file = 'GenomeSet_summary.tsv'
        TSV_path = os.path.join(outdir, TSV_file)
        TSV_str = "\n".join(TSV_table_buf)
        with open(TSV_path, 'w') as TSV_handle:
            TSV_handle.write(TSV_str)
        try:
            TSV_file_save_info = self.dfuClient.file_to_shock({'file_path': TSV_path, 'make_handle': 0})
        except:
            raise ValueError ("error saving TSV_file")
        file_links = [{'shock_id': TSV_file_save_info['shock_id'],
                       'name': TSV_file,
                       'label': 'GenomeSet summary TSV'}]
        
        
        #### build HTML table
        ##
        html_file_path = None
        # config
        head_color = "#eeeeff"
        border_head_color = "#ffccff"
        accept_row_color = 'white'
        #reject_row_color = '#ffeeee'
        reject_row_color = '#eeeeee'
        reject_cell_color = '#ffcccc'
        text_fontsize = "2"
        text_color = '#606060'
        border_body_color = "#cccccc"
        bar_width = 100
        bar_height = 15
        bar_color = "lightblue"
        bar_line_color = "#cccccc"
        bar_fontsize = "1"
        bar_char = "."
        cellpadding = "3"
        cellspacing = "2"
        border = "0"

        # begin buffer and table header
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += ['<p>']

        html_report_lines += ['<table cellpadding='+cellpadding+' cellspacing = '+cellspacing+' border='+border+'>']
        html_report_lines += ['<tr bgcolor="'+head_color+'">']
        html_report_lines += ['<td style="border-right:solid 2px '+border_head_color+'; border-bottom:solid 2px '+border_head_color+'"><font color="'+text_color+'" size='+text_fontsize+'><b>'+'Genome'+'</b></font></td>']
        for field in fields:
            html_report_lines += ['<td style="border-right:solid 2px '+border_head_color+'; border-bottom:solid 2px '+border_head_color+'"><font color="'+text_color+'" size='+text_fontsize+'><b>'+field_titles[field]+'</b></font></td>']
        html_report_lines += ['</tr>']

        # add in data
        for genome_newVer_ref in genome_newVer_ref_order:
            row_color = accept_row_color
            html_report_lines += ['<tr bgcolor="'+row_color+'">']
            genome_obj_name = genome_newVer_ref_to_obj_name[genome_newVer_ref]
            html_report_lines += ['<td style="border-right:solid 1px '+border_body_color+'; border-bottom:solid 1px '+border_body_color+'"><font color="'+text_color+'" size='+text_fontsize+'>'+genome_obj_name+'</font></td>']
            for field in fields:
                if field == 'taxonomy':
                    val = "</nobr><br><nobr>".join(table[genome_newVer_ref][field].split(';'))
                    val = '<nobr>'+val+'</nobr>'
                else:
                    val = str(table[genome_newVer_ref][field])
                html_report_lines += ['<td style="border-right:solid 1px '+border_body_color+'; border-bottom:solid 1px '+border_body_color+'"><font color="'+text_color+'" size='+text_fontsize+'>'+val+'</font></td>']
            html_report_lines += ['</tr>']

        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        # write html to file and upload
        html_report_str = "\n".join(html_report_lines)
        html_file = 'GenomeSet_summary_table.html'
        html_path = os.path.join (html_dir, html_file)
        with open (html_path, 'w') as html_handle:
            html_handle.write(html_report_str)
        try:
            HTML_dir_save_info = self.dfuClient.file_to_shock({'file_path': html_dir,
                                                               'make_handle': 0,
                                                               'pack': 'zip'})
        except:
            raise ValueError ("error saving HTML dir")

        html_links = [{'shock_id': HTML_dir_save_info['shock_id'],
                       'name': html_file,
                       'label': 'GenomeSet summary table HTML'}]
        
        
            
        # build output report object
        self.log(console, "BUILDING REPORT")
        reportName = 'GenomeSet_summary_report'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     'message': '',
                     'direct_html': '',
                     'direct_html_link_index': 0,
                     'file_links': file_links,
                     'html_links': html_links,
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }

        # Save report
        report_info = self.reportClient.create_extended_report(reportObj)
        returnVal = { 'report_name': report_info['name'],
                      'report_ref': report_info['ref'] }
        self.log(console, "KButil_Summarize_GenomeSet DONE")
        #END KButil_Summarize_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Summarize_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
