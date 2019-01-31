# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import sys
import requests
import re
from datetime import datetime
from pprint import pformat  # ,pprint
import uuid

# SDK Utils
from Workspace.WorkspaceClient import Workspace as workspaceService
from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.SetAPIServiceClient import SetAPI
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.kb_uploadmethodsClient import kb_uploadmethods

# silence whining
#import requests
#requests.packages.urllib3.disable_warnings()

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
    VERSION = "1.2.0"
    GIT_URL = "https://github.com/dcchivian/kb_SetUtilities"
    GIT_COMMIT_HASH = "122bed18965da861013cf28e32053bd3ad836e11"

    #BEGIN_CLASS_HEADER
    workspaceURL = None
    shockURL = None
    handleURL = None
    serviceWizardsURL = None
    callbackURL = None
    scratch = None

    # target is a list for collecting log messages
    def log(self, target, message):
        # we should do something better here...
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()

    def get_single_end_read_library(self, ws_data, ws_info, forward):
        pass

    def get_feature_set_seqs(self, ws_data, ws_info):
        pass

    def get_genome_feature_seqs(self, ws_data, ws_info):
        pass

    def get_genome_set_feature_seqs(self, ws_data, ws_info):
        pass

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.serviceWizardURL = config['service-wizard-url']

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
#        if self.callbackURL == None:
#            self.callbackURL = os.environ['SDK_CALLBACK_URL']
        if self.callbackURL is None:
            raise ValueError("SDK_CALLBACK_URL not set in environment")

        self.scratch = os.path.abspath(config['scratch'])
        # HACK!! temp hack for issue where megahit fails on mac because of silent named pipe error
        #self.host_scratch = self.scratch
        #self.scratch = os.path.join('/kb','module','local_scratch')
        # end hack
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

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
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Localize_FeatureSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
#        report = 'Running KButil_FASTQ_to_FASTA with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_ref' not in params:
            raise ValueError('input_ref parameter is required')
        #if 'output_name' not in params:
        #    raise ValueError('output_name parameter is required')

 
        # establish workspace client
        self.log (console, "GETTING WORKSPACE CLIENT")
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)


        # read FeatureSet to get local workspace ID, source object name, and list of original genome refs
        #
        self.log (console, "READING LOCAL WORKSPACE ID")
        src_featureSet_ref = params['input_ref']
        src_featureSet_name = None
        try:
            #objects = wsClient.get_objects([{'ref': src_featureSet_ref}])
            objects = wsClient.get_objects2({'objects': [{'ref': src_featureSet_ref}]})['data']
            data = objects[0]['data']
            info = objects[0]['info']
            src_featureSet_name = info[NAME_I]
            type_name = info[TYPE_I].split('.')[1].split('-')[0]
        except Exception as e:
            raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()
        if type_name != 'FeatureSet':
            raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")
            
        # Set local WSID from FeatureSet
        local_WSID = str(info[WSID_I])

        
        # read workspace to determine which genome objects are already present
        #
        genome_obj_type = "KBaseGenomes.Genome"
        local_genome_refs_by_name = dict()
        try:
            genome_obj_info_list = wsClient.list_objects({'ids':[local_WSID],'type':genome_obj_type})
        except Exception as e:
            raise ValueError ("Unable to list "+genome_obj_type+" objects from workspace: "+str(local_WSID)+" "+str(e))
        for info in genome_obj_info_list:
            genome_obj_ref = str(info[WSID_I])+'/'+str(info[OBJID_I])+'/'+str(info[VERSION_I])
            genome_obj_name = str(info[NAME_I])
            local_genome_refs_by_name[genome_obj_name] = genome_obj_ref


        # set order for features list
        #
        self.log (console, "GETTING FEATURES ORDERING")
        src_featureSet = data
        src_element_ordering = []
        if 'element_ordering' in src_featureSet.keys():
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
                    try:
                        src_genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':src_genome_ref}]})[0]
                        src_genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", src_genome_obj_info[TYPE_I])  # remove trailing version
                    except Exception as e:
                        raise ValueError('Unable to get genome object info from workspace: (' + str(src_genome_ref) +')' + str(e))

                    #acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation"]
                    acceptable_types = ["KBaseGenomes.Genome"]
                    if src_genome_obj_type not in acceptable_types:
                        raise ValueError("Input Genome of type: '" + src_genome_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))
            
                    standardized_src_genome_ref = '{}/{}/{}'.format(src_genome_obj_info[WSID_I],
                                                                    src_genome_obj_info[OBJID_I],
                                                                    src_genome_obj_info[VERSION_I])
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
                try:
                    #objects = wsClient.get_objects([{'ref': this_genome_ref}])
                    objects = wsClient.get_objects2({'objects': [{'ref': src_genome_ref}]})['data']
                    src_genome_obj_data = objects[0]['data']
                    src_genome_obj_info = objects[0]['info']
                except Exception as e:
                    raise ValueError('Unable to fetch this_genome_ref '+str(src_genome_ref)+' object from workspace: ' + str(e))
                    #to get the full stack trace: traceback.format_exc()
                
                # check if genome obj with that name already in local WS
                src_genome_obj_name = src_genome_obj_info[NAME_I]
                if src_genome_obj_name in local_genome_refs_by_name:
                    
                    src2dst_genome_refs[src_genome_ref] = local_genome_refs_by_name[src_genome_obj_name]
                    local_genome_cnt += 1
                    continue
                non_local_genome_cnt += 1

                # load the method provenance from the context object
                provenance = [{}]
                if 'provenance' in ctx:
                    provenance = ctx['provenance']
                # add additional info to provenance here, in this case the input data object reference
                provenance[0]['input_ws_objects'] = []
                provenance[0]['input_ws_objects'].append(src_featureSet_ref)
                provenance[0]['input_ws_objects'].append(src_genome_ref)
                provenance[0]['service'] = 'kb_SetUtilities'
                provenance[0]['method'] = 'KButil_Localize_FeatureSet'
            
                # Save object
                self.log(console, "SAVING GENOME "+str(src_genome_obj_info[NAME_I])+" "+str(src_genome_ref)+" to workspace "+str(params['workspace_name'])+" (ws."+str(local_WSID)+")")  # DEBUG
                dst_genome_obj_data = src_genome_obj_data
                dst_genome_obj_name = src_genome_obj_info[NAME_I]
                dst_genome_obj_info = wsClient.save_objects({
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
                dst_standardized_genome_ref = '{}/{}/{}'.format(dst_genome_obj_info[WSID_I],
                                                                dst_genome_obj_info[OBJID_I],
                                                                dst_genome_obj_info[VERSION_I])
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

            # load the method provenance from the context object
            self.log(console, "SAVING UPDATED FEATURESET")  # DEBUG
            #self.log(console, "SETTING PROVENANCE")  # DEBUG
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']
            # add additional info to provenance here, in this case the input data object reference
            provenance[0]['input_ws_objects'] = []
            provenance[0]['input_ws_objects'].append(src_featureSet_ref)
            provenance[0]['service'] = 'kb_SetUtilities'
            provenance[0]['method'] = 'KButil_Localize_FeatureSet'

            dst_featureSet_info = wsClient.save_objects({
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
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        reportName = 'kb_SetUtilities_localize_featureset_report_' + str(uuid.uuid4())
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Localize_FeatureSet'
        report_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                 'objects': [{'type': 'KBaseReport.Report',
                                                              'data': reportObj,
                                                              'name': reportName,
                                                              'meta': {},
                                                              'hidden': 1,
                                                              'provenance': provenance}]})[0]

        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}".format(report_obj_info[6], report_obj_info[0], report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
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
#        report = 'Running KButil_FASTQ_to_FASTA with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

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
        for featureSet_ref in params['input_refs']:
            if featureSet_ref not in featureSet_seen.keys():
                featureSet_seen[featureSet_ref] = 1
            else:
                self.log("repeat featureSet_ref: '" + featureSet_ref + "'")
                self.log(invalid_msgs, "repeat featureSet_ref: '" + featureSet_ref + "'")
                continue

            try:
                ws = workspaceService(self.workspaceURL, token=ctx['token'])
                #objects = ws.get_objects([{'ref': featureSet_ref}])
                objects = ws.get_objects2({'objects': [{'ref': featureSet_ref}]})['data']
                data = objects[0]['data']
                info = objects[0]['info']
                # Object Info Contents
                # absolute ref = info[6] + '/' + info[0] + '/' + info[4]
                # 0 - obj_id objid
                # 1 - obj_name name
                # 2 - type_string type
                # 3 - timestamp save_date
                # 4 - int version
                # 5 - username saved_by
                # 6 - ws_id wsid
                # 7 - ws_name workspace
                # 8 - string chsum
                # 9 - int size
                # 10 - usermeta meta
                type_name = info[2].split('.')[1].split('-')[0]

            except Exception as e:
                raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            this_featureSet = data
            this_element_ordering = []
            if 'element_ordering' in this_featureSet.keys():
                this_element_ordering = this_featureSet['element_ordering']
            else:
                this_element_ordering = sorted(this_featureSet['elements'].keys())
            element_ordering.extend(this_element_ordering)
            logMsg = 'features in input set {}: {}'.format(featureSet_ref,
                                                           len(this_element_ordering))
            self.log(console, logMsg)
            report += 'features in input set ' + featureSet_ref + ': ' + str(
                len(this_element_ordering)) + "\n"

            for fId in this_featureSet['elements'].keys():
                elements[fId] = this_featureSet['elements'][fId]

        # load the method provenance from the context object
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        for featureSet_ref in params['input_refs']:
            provenance[0]['input_ws_objects'].append(featureSet_ref)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Merge_FeatureSet_Collection'

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING FEATURESET")  # DEBUG
            output_FeatureSet = {'description': params['desc'],
                                 'element_ordering': element_ordering,
                                 'elements': elements}

            new_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                            'objects': [{
                                                'type': 'KBaseCollections.FeatureSet',
                                                'data': output_FeatureSet,
                                                'name': params['output_name'],
                                                'meta': {},
                                                'provenance': provenance}]})

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
        if len(invalid_msgs) == 0:
            self.log(console, "features in output set " + params['output_name'] + ": "
                     + str(len(element_ordering)))
            report += 'features in output set ' + params['output_name'] + ': '
            report += str(len(element_ordering)) + "\n"
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

        reportName = 'kb_SetUtilities_merge_featureset_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                           'objects': [{'type': 'KBaseReport.Report',
                                                        'data': reportObj,
                                                        'name': reportName,
                                                        'meta': {},
                                                        'hidden': 1,
                                                        'provenance': provenance}]})[0]

        # Build report and return
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}".format(report_obj_info[6], report_obj_info[0], report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
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
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        logMsg = ''
        report = ''

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_featureSet_refs' not in params:
            raise ValueError('input_featureSet_refs parameter is required')
        if 'input_genome_refs' not in params:
            raise ValueError('input_genome_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

        # establish workspace client
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)


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
            try:
                genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_genome_ref}]})[0]
                genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", genome_obj_info[TYPE_I])  # remove trailing version
            except Exception as e:
                raise ValueError('Unable to get genome object info from workspace: (' + str(this_genome_ref) +')' + str(e))

            acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation"]
            if genome_obj_type not in acceptable_types:
                raise ValueError("Input Genome of type: '" + genome_obj_type +
                                 "'.  Must be one of " + ", ".join(acceptable_types))
            
            this_standardized_genome_ref = '{}/{}/{}'.format(genome_obj_info[WSID_I],
                                                             genome_obj_info[OBJID_I],
                                                             genome_obj_info[VERSION_I])
            genome_ref_to_standardized[this_genome_ref] = this_standardized_genome_ref
            genome_ref_from_standardized_in_input_flag[this_standardized_genome_ref] = True


        # Build FeatureSets
        #
        featureSet_seen = dict()
        featureSet_genome_ref_to_standardized = dict()  # have to map genome refs in featureSets also because might be mixed WS_ID-WS_NAME/OBJID-OBJNAME and not exactly correspond with input genome refs
        feature_list_lens = []
        objects_created = []

        for featureSet_ref in params['input_featureSet_refs']:
            if featureSet_ref not in featureSet_seen.keys():
                featureSet_seen[featureSet_ref] = 1
            else:
                self.log("repeat featureSet_ref: '" + featureSet_ref + "'")
                self.log(invalid_msgs, "repeat featureSet_ref: '" + featureSet_ref + "'")
                continue

            try:
                #objects = wsClient.get_objects([{'ref': featureSet_ref}])
                objects = wsClient.get_objects2({'objects': [{'ref': featureSet_ref}]})['data']
                data = objects[0]['data']
                info = objects[0]['info']
                # Object Info Contents
                # absolute ref = info[6] + '/' + info[0] + '/' + info[4]
                # 0 - obj_id objid
                # 1 - obj_name name
                # 2 - type_string type
                # 3 - timestamp save_date
                # 4 - int version
                # 5 - username saved_by
                # 6 - ws_id wsid
                # 7 - ws_name workspace
                # 8 - string chsum
                # 9 - int size
                # 10 - usermeta meta
                this_featureSet_obj_name = info[1]
                type_name = info[2].split('.')[1].split('-')[0]

            except Exception as e:
                raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")
                
            this_featureSet = data

            this_element_ordering = []
            if 'element_ordering' in this_featureSet.keys():
                this_element_ordering = this_featureSet['element_ordering']
            else:
                this_element_ordering = sorted(this_featureSet['elements'].keys())
            logMsg = 'features in input set {}: {}'.format(featureSet_ref,
                                                           len(this_element_ordering))
            self.log(console, logMsg)


            # Build sliced FeatureSet
            #
            self.log (console, "BUILDING SLICED FEATURESET\n")  # DEBUG
            self.log (console, "Slicing out genomes "+("\n".join(params['input_genome_refs'])))  # DEBUG
            element_ordering = []
            elements = {}
            for fId in this_element_ordering:
                #self.log (console, 'checking feature {}'.format(fId))  # DEBUG
                feature_hit = False
                genomes_retained = []
                for this_genome_ref in this_featureSet['elements'][fId]:
                    genome_hit = False
                    #self.log (console, "\t"+'checking genome {}'.format(this_genome_ref))  # DEBUG

                    #if this_genome_ref in params['input_genome_refs']:   # The KEY line 
                    if this_genome_ref in genome_ref_to_standardized:
                        genome_hit = True
                        standardized_genome_ref = genome_ref_to_standardized[this_genome_ref]
                    elif this_genome_ref in featureSet_genome_ref_to_standardized:
                        standardized_genome_ref = featureSet_genome_ref_to_standardized[this_genome_ref]
                        if standardized_genome_ref in genome_ref_from_standardized_in_input_flag:
                            genome_hit = True
                    else:  # get standardized genome_ref
                        try:
                            genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_genome_ref}]})[0]
                            genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", genome_obj_info[TYPE_I])  # remove trailing version
                        except Exception as e:
                            raise ValueError('Unable to get genome object info from workspace: (' + str(this_genome_ref) +')' + str(e))

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation"]
                        if genome_obj_type not in acceptable_types:
                            raise ValueError("Input Genome of type: '" + genome_obj_type +
                                             "'.  Must be one of " + ", ".join(acceptable_types))
            
                        standardized_genome_ref = '{}/{}/{}'.format(genome_obj_info[WSID_I],
                                                                    genome_obj_info[OBJID_I],
                                                                    genome_obj_info[VERSION_I])
                        featureSet_genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref
                        if standardized_genome_ref in genome_ref_from_standardized_in_input_flag:
                            genome_hit = True

                    if genome_hit:
                        #self.log (console, "\t"+'GENOME HIT')  # DEBUG
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
                # load the method provenance from the context object
                self.log(console, "SETTING PROVENANCE")  # DEBUG
                provenance = [{}]
                if 'provenance' in ctx:
                    provenance = ctx['provenance']
                # add additional info to provenance here, in this case the input data object reference
                provenance[0]['input_ws_objects'] = []
                provenance[0]['input_ws_objects'].append(featureSet_ref)
                for genome_ref in params['input_genome_refs']:
                    provenance[0]['input_ws_objects'].append(genome_ref)
                provenance[0]['service'] = 'kb_SetUtilities'
                provenance[0]['method'] = 'KButil_Slice_FeatureSets_by_Genome'

                # Store output object
                if len(invalid_msgs) == 0:
                    self.log(console, "SAVING FEATURESET")  # DEBUG
                    output_FeatureSet = {'description': params['desc'],
                                         'element_ordering': element_ordering,
                                         'elements': elements}

                    output_name = params['output_name']
                    if len(params['input_featureSet_refs']) > 1:
                        output_name += '-' + this_featureSet_obj_name

                    new_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                          'objects': [{
                                                              'type': 'KBaseCollections.FeatureSet',
                                                              'data': output_FeatureSet,
                                                              'name': output_name,
                                                              'meta': {},
                                                              'provenance': provenance}]})
                
                    feature_list_lens.append(len(element_ordering))
                    objects_created.append({'ref': params['workspace_name'] + '/' + output_name,
                                            'description': params['desc']})


        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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

        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        for featureSet_ref in params['input_featureSet_refs']:
            provenance[0]['input_ws_objects'].append(featureSet_ref)
        for genome_ref in params['input_genome_refs']:
            provenance[0]['input_ws_objects'].append(genome_ref)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Slice_FeatureSets_by_Genome'

        reportName = 'kb_SetUtilities_slice_featureset_by_genomes_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                 'objects': [{'type': 'KBaseReport.Report',
                                                              'data': reportObj,
                                                              'name': reportName,
                                                              'meta': {},
                                                              'hidden': 1,
                                                              'provenance': provenance}]})[0]
        
        # Build report and return
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}".format(report_obj_info[6], report_obj_info[0], report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
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
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        logMsg = ''
        report = ''
        genome_id_feature_id_delim = ".f:"
        

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'operator' not in params:
            raise ValueError('operator parameter is required')
        if 'input_featureSet_ref_A' not in params:
            raise ValueError('input_featureSet_ref_A parameter is required')
        if 'input_featureSet_ref_B' not in params:
            raise ValueError('input_featureSet_ref_B parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

        # establish workspace client
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)


        # Get FeatureSets
        #
        FeatureSet = dict()
        FeatureSet['A'] = dict()
        FeatureSet['B'] = dict()
        input_featureSet_refs = dict()
        input_featureSet_refs['A'] = params['input_featureSet_ref_A']
        input_featureSet_refs['B'] = params['input_featureSet_ref_B']
        for set_id in ['A','B']:
            try:
                #objects = wsClient.get_objects([{'ref': featureSet_ref}])
                objects = wsClient.get_objects2({'objects': [{'ref': input_featureSet_refs[set_id]}]})['data']
                data = objects[0]['data']
                info = objects[0]['info']
                this_featureSet = data
                this_featureSet_obj_name = info[NAME_I]
                type_name = info[TYPE_I].split('.')[1].split('-')[0]
            except Exception as e:
                raise ValueError('Unable to fetch input_featureSet_ref '+str(input_featureSet_refs[set_id])+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()
            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            FeatureSet[set_id] = this_featureSet
            if 'element_ordering' not in this_featureSet.keys():
                FeatureSet[set_id]['element_ordering'] = sorted(this_featureSet['elements'].keys())
            logMsg = 'features in input set {}: {}'.format(input_featureSet_refs[set_id],
                                                           len(FeatureSet[set_id]['element_ordering']))
            self.log(console, logMsg)


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
                        standardized_genome_ref = featureSet_genome_ref_to_standardized[this_genome_ref]
                    else:  # get standardized genome_ref
                        try:
                            genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_genome_ref}]})[0]
                            genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", genome_obj_info[TYPE_I])  # remove trailing version
                        except Exception as e:
                            raise ValueError('Unable to get genome object info from workspace: (' + str(this_genome_ref) +')' + str(e))

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation"]
                        if genome_obj_type not in acceptable_types:
                            raise ValueError("Input Genome of type: '" + genome_obj_type +
                                             "'.  Must be one of " + ", ".join(acceptable_types))
            
                        standardized_genome_ref = '{}/{}/{}'.format(genome_obj_info[WSID_I],
                                                                    genome_obj_info[OBJID_I],
                                                                    genome_obj_info[VERSION_I])
                        featureSet_genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref
                    feature_standardized_genome_refs.append(standardized_genome_ref)  # standardize list
                    combo_id = standardized_genome_ref + genome_id_feature_id_delim + fId
                    genome_feature_present[set_id][combo_id] = True
                FeatureSet[set_id]['elements'][fId] = feature_standardized_genome_refs


        # Build sliced FeatureSet
        #
        self.log (console, "BUILDING SLICED FEATURESET\n")  # DEBUG
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
            #self.log (console, 'checking feature {}'.format(fId))  # DEBUG
            feature_hit = False
            genomes_retained = []
            for this_genome_ref in FeatureSet[fwd_set_id]['elements'][fId]:
                combo_id = this_genome_ref + genome_id_feature_id_delim + fId
                #self.log (console, "\t"+'checking genome {}'.format(this_genome_ref))  # DEBUG

                if params['operator'] == 'yesA_yesB':
                    try:
                        seen = genome_feature_present[rev_set_id][combo_id]
                        feature_hit = True
                        genomes_retained.append(this_genome_ref)
                    except:
                        pass
                else:
                    try:
                        seen = genome_feature_present[rev_set_id][combo_id]
                        pass
                    except:
                        feature_hit = True
                        genomes_retained.append(this_genome_ref)
                   
            if feature_hit:
                output_element_ordering.append(fId)
                output_elements[fId] = genomes_retained
        logMsg = 'features in sliced output set: {}'.format(len(output_element_ordering))
        self.log(console, logMsg)


        # Save output FeatureSet
        #
        objects_created = []

        # load the method provenance from the context object
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(input_featureSet_refs['A'])
        provenance[0]['input_ws_objects'].append(input_featureSet_refs['B'])
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Logical_Slice_Two_FeatureSets'

        if len(output_element_ordering) == 0:
            report += 'no features to output under operator '+params['operator']+"\n"

        else:

            # Store output object
            if len(invalid_msgs) == 0:
                self.log(console, "SAVING FEATURESET")  # DEBUG
                output_FeatureSet = {'description': params['desc'],
                                     'element_ordering': output_element_ordering,
                                     'elements': output_elements}

                output_name = params['output_name']

                new_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                      'objects': [{
                                                          'type': 'KBaseCollections.FeatureSet',
                                                          'data': output_FeatureSet,
                                                          'name': output_name,
                                                          'meta': {},
                                                          'provenance': provenance}]})
                
                objects_created.append({'ref': params['workspace_name'] + '/' + output_name,
                                        'description': params['desc']})

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_logical_slice_two_featuresets_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                 'objects': [{'type': 'KBaseReport.Report',
                                                              'data': reportObj,
                                                              'name': reportName,
                                                              'meta': {},
                                                              'hidden': 1,
                                                              'provenance': provenance}]})[0]
        
        # Build report and return
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}".format(report_obj_info[6], report_obj_info[0], report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
        self.log(console, "KButil_Logical_Slice_Two_FeatureSets DONE")
        #END KButil_Logical_Slice_Two_FeatureSets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Logical_Slice_Two_FeatureSets return value ' +
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
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Merge_GenomeSets with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
#        report = 'Running KButil_Merge_GenomeSets with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 2:
            self.log(console, "Must provide at least two GenomeSets")
            self.log(invalid_msgs, "Must provide at least two GenomeSets")

        # load the method provenance from the context object
        #
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        try:
            prov_defined = provenance[0]['input_ws_objects']
        except:
            provenance[0]['input_ws_objects'] = []
        for input_genomeset_ref in params['input_refs']:
            provenance[0]['input_ws_objects'].append(input_genomeset_ref)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Merge_GenomeSets'

        # Build GenomeSet
        #
        elements = dict()

        # Add Genomes from GenomeSets
        for input_genomeset_ref in params['input_refs']:

            try:
                ws = workspaceService(self.workspaceURL, token=ctx['token'])
                #objects = ws.get_objects([{'ref': input_genomeset_ref}])
                objects = ws.get_objects2({'objects': [{'ref': input_genomeset_ref}]})['data']
                genomeSet = objects[0]['data']
                info = objects[0]['info']
               
                type_name = info[2].split('.')[1].split('-')[0]
                if type_name != 'GenomeSet':
                    raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")
            except Exception as e:
                raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            for gId in genomeSet['elements'].keys():
                genomeRef = genomeSet['elements'][gId]['ref']
                try:
                    already_included = elements[gId]
                except:
                    elements[gId] = dict()
                    elements[gId]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element " + gId + " : " + genomeRef)  # DEBUG

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")  # DEBUG
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements
                                }

            new_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                            'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                         'data': output_GenomeSet,
                                                         'name': params['output_name'],
                                                         'meta': {},
                                                         'provenance': provenance
                                                         }]
                                            })

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                              str(len(elements.keys())))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(elements.keys())) + "\n"
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

        reportName = 'kb_SetUtilities_merge_genomesets_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                           'objects': [{'type': 'KBaseReport.Report',
                                                        'data': reportObj,
                                                        'name': reportName,
                                                        'meta': {},
                                                        'hidden': 1,
                                                        'provenance': provenance}]})[0]

        # Build report and return
        #
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{0}/{1}/{2}".format(report_obj_info[6], report_obj_info[0],
                                          report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
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

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

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

            try:
                already_included = genome_seen[genomeRef]
            except:
                genome_seen[genomeRef] = True

                try:
                    ws = workspaceService(self.workspaceURL, token=ctx['token'])
                    #objects = ws.get_objects([{'ref': genomeRef}])
                    objects = ws.get_objects2({'objects': [{'ref': genomeRef}]})['data']
                    data = objects[0]['data']
                    info = objects[0]['info']
                    genomeObj = data
                    obj_name = info[1]
                    type_name = info[2].split('.')[1].split('-')[0]
                except Exception as e:
                    raise ValueError('Unable to fetch input_name object from workspace: ' + str(e))
                if type_name != 'Genome' and type_name != 'GenomeAnnotation':
                    errMsg = "Bad Type: Should be Genome or GenomeAnnotation not '{}' for ref: '{}'"
                    raise ValueError(errMsg.format(type_name, genomeRef))

                if type_name == 'Genome':
                    genome_id = genomeObj['id']
                else:
                    genome_id = genomeObj['genome_annotation_id']
                genome_sci_name = genomeObj['scientific_name']

                #if not genome_id in elements.keys():
                #    elements[genome_id] = dict()
                #elements[genome_id]['ref'] = genomeRef  # the key line
                if genomeRef not in elements.keys(): 
                    elements[genomeRef] = dict()
                elements[genomeRef]['ref'] = genomeRef  # the key line
                self.log(console, "adding element {} ({}) aka ({}): {}".format(obj_name,
                                                                               genome_sci_name,
                                                                               genome_id,
                                                                               genomeRef))  # DEBUG

        # load the method provenance from the context object
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        for genomeRef in params['input_refs']:
            provenance[0]['input_ws_objects'].append(genomeRef)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Build_GenomeSet'

        # Store output object
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")  # DEBUG
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                            'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                         'data': output_GenomeSet,
                                                         'name': params['output_name'],
                                                         'meta': {},
                                                         'provenance': provenance}]})

        # build output report object
        #
        self.log(console, "BUILDING REPORT")  # DEBUG
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] +
                              ": " + str(len(elements.keys())))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(elements.keys())) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Build_GenomeSet'}],
                'text_message': report
            }
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        reportName = 'kb_SetUtilities_build_genomeset_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                           'objects': [{'type': 'KBaseReport.Report',
                                                        'data': reportObj,
                                                        'name': reportName,
                                                        'meta': {},
                                                        'hidden': 1,
                                                        'provenance': provenance}]})[0]

        # Build report and return
        #
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}".format(report_obj_info[6], report_obj_info[0], report_obj_info[4])
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref}
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
#        report = 'Running KButil_Build_GenomeSet_from_FeatureSet with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_ref' not in params:
            raise ValueError('input_ref parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

        # Obtain FeatureSet
        try:
            ws = workspaceService(self.workspaceURL, token=ctx['token'])
            #objects = ws.get_objects([{'ref': params['input_ref']}])
            objects = ws.get_objects2({'objects': [{'ref': params['input_ref']}]})['data']
            data = objects[0]['data']
            info = objects[0]['info']
            # Object Info Contents
            # absolute ref = info[6] + '/' + info[0] + '/' + info[4]
            # 0 - obj_id objid
            # 1 - obj_name name
            # 2 - type_string type
            # 3 - timestamp save_date
            # 4 - int version
            # 5 - username saved_by
            # 6 - ws_id wsid
            # 7 - ws_name workspace
            # 8 - string chsum
            # 9 - int size
            # 10 - usermeta meta
            featureSet = data
            type_name = info[2].split('.')[1].split('-')[0]
        except Exception as e:
            raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()
        if type_name != 'FeatureSet':
            raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

        # Build GenomeSet
        elements = {}
        genome_seen = dict()

        for fId in featureSet['elements'].keys():
            for genomeRef in featureSet['elements'][fId]:

                try:
                    already_included = genome_seen[genomeRef]
                except:
                    genome_seen[genomeRef] = True

                    try:
                        ws = workspaceService(self.workspaceURL, token=ctx['token'])
                        #objects = ws.get_objects([{'ref': genomeRef}])
                        objects = ws.get_objects2({'objects': [{'ref': genomeRef}]})['data']
                        data = objects[0]['data']
                        info = objects[0]['info']
                        genomeObj = data
                        obj_name = info[1]
                        type_name = info[2].split('.')[1].split('-')[0]
                    except Exception as e:
                        errMsg = 'Unable to fetch genomeRef object from workspace: ' + str(e)
                        raise ValueError(errMsg)
                    if type_name != 'Genome' and type_name != 'GenomeAnnotaton':
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
                    if genomeRef not in elements.keys(): 
                        elements[genomeRef] = dict()
                    elements[genomeRef]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element {} ({}/{}) : {}".format(obj_name,
                                                                              genome_sci_name,
                                                                              genome_id,
                                                                              genomeRef))  # DEBUG

        # load the method provenance from the context object
        #
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(params['input_ref'])
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Build_GenomeSet_from_FeatureSet'

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")  # DEBUG
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                            'objects': [{'type': 'KBaseSearch.GenomeSet',
                                                         'data': output_GenomeSet,
                                                         'name': params['output_name'],
                                                         'meta': {},
                                                         'provenance': provenance}]})

        # build output report object
        #
        self.log(console, "BUILDING REPORT")  # DEBUG
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                     str(len(elements.keys())))
            report += 'genomes in output set {}:{}\n'.format(params['output_name'],
                                                             len(elements.keys()))
            ref = "{}/{}".format(params['workspace_name'], params['output_name'])
            reportObj = {'objects_created': [{'ref': ref,
                         'description': 'KButil_Build_GenomeSet_from_FeatureSet'}],
                         'text_message': report}
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        reportName = 'kb_SetUtilities_build_genomeset_from_featureset_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                           'objects': [{'type': 'KBaseReport.Report',
                                                        'data': reportObj,
                                                        'name': reportName,
                                                        'meta': {},
                                                        'hidden': 1,
                                                        'provenance': provenance}]})[0]

        # Build report and return
        self.log(console, "BUILDING RETURN OBJECT")
        returnVal = {'report_name': reportName,
                     'report_ref': "{}/{}/{}".format(report_obj_info[6], report_obj_info[0],
                                                     report_obj_info[4])}
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
           parameter "input_genome_refs" of type "data_obj_ref", parameter
           "input_genomeset_ref" of type "data_obj_ref", parameter
           "output_name" of type "data_obj_name", parameter "desc" of String
        :returns: instance of type "KButil_Add_Genomes_to_GenomeSet_Output"
           -> structure: parameter "report_name" of type "data_obj_name",
           parameter "report_ref" of type "data_obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN KButil_Add_Genomes_to_GenomeSet

        # init
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Add_Genomes_to_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
#        report = 'Running KButil_Add_Genomes_to_GenomeSet with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_genome_refs' not in params:
            raise ValueError('input_genome_refs parameter is required')
        if 'input_genomeset_ref' not in params:
            raise ValueError('input_genomeset_ref parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

        # Build GenomeSet
        elements = dict()

        # add old GenomeSet
        #
        if 'input_genomeset_ref' in params and params['input_genomeset_ref'] is not None:
            try:
                #objects = ws.get_objects([{'ref': params['input_genomeset_ref']}])
                objects = ws.get_objects2(
                    {'objects': [{'ref': params['input_genomeset_ref']}]})['data']
                genomeSet = objects[0]['data']
                info = objects[0]['info']

                type_name = info[2].split('.')[1].split('-')[0]
                if type_name != 'GenomeSet':
                    raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")
            except Exception as e:
                raise ValueError('Unable to fetch input_ref object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            for gId in genomeSet['elements'].keys():
                genomeRef = genomeSet['elements'][gId]['ref']
                try:
                    already_included = elements[gId]
                except:
                    elements[gId] = dict()
                    elements[gId]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element " + gId + " : " + genomeRef)  # DEBUG
            
        # add new genome
        for genomeRef in params['input_genome_refs']:

            try:
                #objects = ws.get_objects([{'ref': genomeRef}])
                objects = ws.get_objects2({'objects': [{'ref': genomeRef}]})['data']
                genomeObj = objects[0]['data']
                info = objects[0]['info']
                obj_name = info[1]
                type_name = info[2].split('.')[1].split('-')[0]
                if type_name != 'Genome':
                    errMsg = "Bad Type: Should be Genome or GenomeAnnotation instead of '{}'"
                    raise ValueError(errMsg.format(type_name))

            except Exception as e:
                raise ValueError('Unable to fetch input_name object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            #gId = genomeObj['id']
            #if gId == 'Unknown':
            #    gId = genomeRef
            gId = genomeRef
            try:
                already_included = elements[gId]
            except:
                elements[gId] = dict()
                elements[gId]['ref'] = genomeRef  # the key line
                self.log(console, "adding new element " + gId + " : " + genomeRef)  # DEBUG

        # load the method provenance from the context object
        #
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        try:
            prov_defined = provenance[0]['input_ws_objects']
        except:
            provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(params['input_genomeset_ref'])
        provenance[0]['input_ws_objects'].extend(params['input_genome_refs'])
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Add_Genomes_to_GenomeSet'

        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING GENOMESET")  # DEBUG
            output_GenomeSet = {'description': params['desc'],
                                'elements': elements}

            new_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                            'objects': [{
                                                'type': 'KBaseSearch.GenomeSet',
                                                'data': output_GenomeSet,
                                                'name': params['output_name'],
                                                'meta': {},
                                                'provenance': provenance}]})

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
        if len(invalid_msgs) == 0:
            self.log(console, "genomes in output set " + params['output_name'] + ": " +
                     str(len(elements.keys())))
            report += 'genomes in output set ' + params['output_name'] + ': '
            report += str(len(elements.keys())) + "\n"
            reportObj = {
                'objects_created': [{'ref': params['workspace_name'] + '/' + params['output_name'],
                                     'description':'KButil_Add_Genomes_to_GenomeSet'}],
                'text_message': report}
        else:
            report += "FAILURE:\n\n" + "\n".join(invalid_msgs) + "\n"
            reportObj = {'objects_created': [],
                         'text_message': report}

        reportName = 'kb_SetUtilities_add_genomes_to_genomeset_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({
                'workspace':params['workspace_name'],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1,
                        'provenance':provenance
                    }
                ]
            })[0]

        # Build report and return
        #
        self.log(console,"BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}"
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref.format(report_obj_info[6], report_obj_info[0],
                                                     report_obj_info[4])}
        self.log(console, "KButil_Add_Genomes_to_GenomeSet DONE")
        #END KButil_Add_Genomes_to_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Add_Genomes_to_GenomeSet return value ' +
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

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

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

        # DEBUG
        #params['input_refs'] = ['18858/2/1', '18858/5/1']

        for libRef in params['input_refs']:

            try:
                already_included = lib_seen[libRef]
            except:
                lib_seen[libRef] = True

                try:
                    ws = workspaceService(self.workspaceURL, token=ctx['token'])
                    #objects = ws.get_objects([{'ref': libRef}])
                    objects = ws.get_objects2({'objects':[{'ref': libRef}]})['data']
                    data = objects[0]['data']
                    info = objects[0]['info']
                    libObj = data
                    NAME_I = 1
                    TYPE_I = 2
                    lib_name = info[NAME_I]
                    lib_type = info[TYPE_I].split('.')[1].split('-')[0]

                    if set_type is not None:
                        if lib_type != set_type:
                            raise ValueError("Don't currently support heterogeneous ReadsSets." +
                                             "You have more than one type in your input")
                        set_type = lib_type
                except Exception as e:
                    raise ValueError('Unable to fetch input_name object from workspace: ' + str(e))
                if lib_type != 'SingleEndLibrary' and lib_type != 'PairedEndLibrary':
                    errMsg = "Bad Type: Should be SingleEndLibrary or PairedEndLibrary instead of "
                    errMsg += "'{}' for ref: '{}'"
                    raise ValueError(errMsg.format(lib_type, libRef))

                # add lib
                self.log(console, "adding lib " + lib_name + " : " + libRef)  # DEBUG
                items.append({'ref': libRef, 'label': lib_name})

        # load the method provenance from the context object
        #
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        for libRef in params['input_refs']:
            provenance[0]['input_ws_objects'].append(libRef)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Build_ReadsSet'


        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console, "SAVING READS_SET")  # DEBUG

            try:
                setAPI_Client = SetAPI(url=self.serviceWizardURL, token=ctx['token'])
            except Exception as e:
                raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))

            output_readsSet_obj = {'description': params['desc'],
                                   'items': items}
            output_readsSet_name = params['output_name']
            try:
                rSet_ref = setAPI_Client.save_reads_set_v1(
                    {'workspace_name': params['workspace_name'],
                     'output_object_name': output_readsSet_name,
                     'data': output_readsSet_obj})['set_ref']
            except Exception as e:
                errMsg = 'SetAPI Error: Unable to save read library set obj to workspace: ({})\n{}'
                raise ValueError(errMsg.format(params['workspace_name'], str(e)))

        # build output report object
        #
        self.log(console, "SAVING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_build_readsset_report_' + str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({'workspace': params['workspace_name'],
                                           'objects': [{
                                               'type': 'KBaseReport.Report',
                                               'data': reportObj,
                                               'name': reportName,
                                               'meta': {},
                                               'hidden': 1,
                                               'provenance': provenance}]})[0]

        # Build report and return
        self.log(console, "BUILDING RETURN OBJECT")
        report_ref = "{}/{}/{}"
        returnVal = {'report_name': reportName,
                     'report_ref': report_ref.format(report_obj_info[6], report_obj_info[0],
                                                     report_obj_info[4])}
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

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'

        # param checks
        required_params = ['workspace_name',
                           'input_refs', 
                           'output_name'
                           ]
        for required_param in required_params:
            if required_param not in params or params[required_param] == None:
                raise ValueError ("Must define required param: '"+required_param+"'")

        # clean input_refs
        clean_input_refs = []
        for ref in params['input_refs']:
            if ref is not None and ref != '' and ref not in clean_input_refs:
                clean_input_refs.append(ref)
        params['input_refs'] = clean_input_refs

        if len(params['input_refs']) < 2:
            self.log(console,"Must provide at least two ReadsSets")
            self.log(invalid_msgs,"Must provide at least two ReadsSets")

            
        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=params['input_refs']


        # init output object fields and SetAPI
        combined_readsSet_ref_list   = []
        combined_readsSet_name_list  = []
        combined_readsSet_label_list = []
        try:
            setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
        except Exception as e:
            raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))


        # Iterate through list of ReadsSets
        #
        reads_lib_type = None
        reads_lib_ref_seen = dict()
        accepted_libs = []
        repeat_libs = []
        for set_i,this_readsSet_ref in enumerate(params['input_refs']):
            accepted_libs.append([])
            repeat_libs.append([])
            try:
                # object_info tuple
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)
                
                input_reads_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_readsSet_ref}]})[0]
                input_reads_obj_type = input_reads_obj_info[TYPE_I]
                input_reads_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_reads_obj_type)  # remove trailing version

            except Exception as e:
                raise ValueError('Unable to get readsSet object from workspace: (' + str(this_readsSet_ref) +')' + str(e))

            acceptable_types = ["KBaseSets.ReadsSet"]
            if input_reads_obj_type not in acceptable_types:
                raise ValueError("Input reads of type: '" + input_reads_obj_type +
                                 "'.  Must be one of " + ", ".join(acceptable_types))

            # iterate through read libraries in read set and add new ones to combined ReadsSet
            try:
                input_readsSet_obj = setAPI_Client.get_reads_set_v1({
                    'ref': this_readsSet_ref,
                    'include_item_info': 1})
            except Exception as e:
                raise ValueError('SetAPI Error: Unable to get read library set from workspace: (' +
                                 this_readsSet_ref + ")\n" + str(e))

            NAME_I = 1
            TYPE_I = 2
            for readsLibrary_obj in input_readsSet_obj['data']['items']:
                this_readsLib_ref    = readsLibrary_obj['ref']
                this_readsLib_label  = readsLibrary_obj['label']
                this_readsLib_name   = readsLibrary_obj['info'][NAME_I]
                this_readsLib_type   = readsLibrary_obj['info'][TYPE_I]
                # remove trailing version
                this_readsLib_type   = re.sub ('-[0-9]+\.[0-9]+$', "", this_readsLib_type)
                if reads_lib_type == None:
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
            output_readsSet_ref = setAPI_Client.save_reads_set_v1 ({'workspace_name': params['workspace_name'],
                                                                    'output_object_name': output_readsSet_name,
                                                                    'data': output_readsSet_obj
                                                                    })['set_ref']
        except Exception as e:
            raise ValueError('SetAPI FAILURE: Unable to save read library set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        # build report
        #
        self.log (console, "SAVING REPORT")  # DEBUG        
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
        report = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})

        returnVal = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }
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
#        report = 'Running KButil_Build_AssemblySet with params='
#        report += "\n"+pformat(params)


        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'desc' not in params:
            raise ValueError('desc parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')

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
        
        # DEBUG
        #params['input_refs'] = ['18858/2/1', '18858/5/1']

        for assRef in params['input_refs']:

            try:
                already_included = ass_seen[assRef]
            except:
                ass_seen[assRef] = True

                try:
                    ws = workspaceService(self.workspaceURL, token=ctx['token'])
                    #objects = ws.get_objects([{'ref': assRef}])
                    objects = ws.get_objects2({'objects':[{'ref': assRef}]})['data']
                    data = objects[0]['data']
                    info = objects[0]['info']
                    assObj = data
                    NAME_I = 1
                    TYPE_I = 2
                    ass_name = info[NAME_I]
                    ass_type = info[TYPE_I].split('.')[1].split('-')[0]

                    if set_type != None:
                        if ass_type != set_type:
                            raise ValueError ("Don't currently support heterogeneous AssemblySets.  You have more than one type in your input")
                        set_type = ass_type
                except Exception as e:
                    raise ValueError('Unable to fetch input_name object from workspace: ' + str(e))
                    
                # add assembly
                self.log(console,"adding assembly "+ass_name+" : "+assRef)  # DEBUG
                items.append ({'ref': assRef,
                               'label': ass_name
                               #'data_attachment': ,
                               #'info'
                               })

        # load the method provenance from the context object
        #
        self.log(console,"SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        for assRef in params['input_refs']:
            provenance[0]['input_ws_objects'].append(assRef)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Build_AssemblySet'


        # Store output object
        #
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING ASSEMBLY_SET")  # DEBUG

            try:
                setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
            except Exception as e:
                raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))

            output_assemblySet_obj = { 'description': params['desc'],
                                       'items': items
                                     }
            output_assemblySet_name = params['output_name']
            try:
                output_assemblySet_ref = setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                        'output_object_name': output_assemblySet_name,
                                                                        'data': output_assemblySet_obj
                                                                        })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        # build output report object
        #
        self.log(console,"SAVING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_build_assemblyset_report_'+str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({
#                'id':info[6],
                'workspace':params['workspace_name'],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1,
                        'provenance':provenance
                    }
                ]
            })[0]


        # Build report and return
        #
        self.log(console,"BUILDING RETURN OBJECT")
        returnVal = { 'report_name': reportName,
                      'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]),
                      }
        self.log(console,"KButil_Build_AssemblySet DONE")
        #END KButil_Build_AssemblySet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Build_AssemblySet return value ' +
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
        #END KButil_Batch_Create_GenomeSet

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method KButil_Batch_Create_GenomeSet return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
