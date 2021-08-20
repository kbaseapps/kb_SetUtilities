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
    VERSION = "1.7.6"
    GIT_URL = "https://github.com/kbaseapps/kb_SetUtilities"
    GIT_COMMIT_HASH = "db160f725f75ef9761201f32f19430c8d5c4991b"

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
            raise ValueError('Unable to fetch input_ref '+src_featureSet_ref+' object from workspace: ' + str(e))
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
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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
                raise ValueError('Unable to fetch input_ref '+featureSet_ref+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            this_featureSet = data
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
                                                'provenance': provenance}]})[0]

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_featureSet_refs' not in params:
            raise ValueError('input_featureSet_refs parameter is required')
        if 'input_genome_refs' not in params:
            raise ValueError('input_genome_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced FeatureSet'

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

            acceptable_types = ["KBaseGenomes.Genome", "KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
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
            if featureSet_ref not in list(featureSet_seen.keys()):
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
                raise ValueError('Unable to fetch input_ref '+featureSet_ref+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            if type_name != 'FeatureSet':
                raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

            this_featureSet = data

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

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
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
                                                              'provenance': provenance}]})[0]

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
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple
        logMsg = ''
        report = ''
        genome_id_feature_id_delim = ".f:"


        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'operator' not in params:
            raise ValueError('operator parameter is required')
        if 'input_featureSet_ref_A' not in params:
            raise ValueError('input_featureSet_ref_A parameter is required')
        if 'input_featureSet_ref_B' not in params:
            raise ValueError('input_featureSet_ref_B parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced FeatureSet'

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
                        try:
                            genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_genome_ref}]})[0]
                            genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", genome_obj_info[TYPE_I])  # remove trailing version
                        except Exception as e:
                            raise ValueError('Unable to get genome object info from workspace: (' + str(this_genome_ref) +')' + str(e))

                        acceptable_types = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.GenomeAnnotation","KBaseMetagenomes.AnnotatedMetagenomeAssembly"]
                        if genome_obj_type not in acceptable_types:
                            raise ValueError("Input Genome of type: '" + genome_obj_type +
                                             "'.  Must be one of " + ", ".join(acceptable_types))

                        #standardized_genome_ref = '{}/{}/{}'.format(genome_obj_info[WSID_I],
                        #                                            genome_obj_info[OBJID_I],
                        #                                            genome_obj_info[VERSION_I])
                        standardized_genome_ref_noVer = '{}/{}'.format(genome_obj_info[WSID_I],
                                                                       genome_obj_info[OBJID_I])
                        featureSet_genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref_noVer
                    feature_standardized_genome_refs.append(standardized_genome_ref_noVer)  # standardize list
                    combo_id = standardized_genome_ref_noVer + genome_id_feature_id_delim + fId
                    genome_feature_present[set_id][combo_id] = True
                    self.log(console,"Set {} contains {}".format(set_id,combo_id))  # DEBUG
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
            for this_genome_ref_noVer in FeatureSet[fwd_set_id]['elements'][fId]:
                combo_id = this_genome_ref_noVer + genome_id_feature_id_delim + fId
                self.log (console, "\t"+'checking set {} genome+fid: {}'.format(fwd_set_id,combo_id))  # DEBUG

                if params['operator'] == 'yesA_yesB':
                    if genome_feature_present[rev_set_id].get(combo_id):
                        feature_hit = True
                        genomes_retained.append(this_genome_ref_noVer)
                        self.log(console, "keeping feature {}".format(combo_id))  # DEBUG
                else:
                    if not genome_feature_present[rev_set_id].get(combo_id):
                        feature_hit = True
                        genomes_retained.append(this_genome_ref_noVer)
                        self.log(console, "keeping feature {}".format(combo_id))  # DEBUG

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
                                                          'provenance': provenance}]})[0]

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


        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'operator' not in params:
            raise ValueError('operator parameter is required')
        if 'input_assemblySet_ref_A' not in params:
            raise ValueError('input_assemblySet_ref_A parameter is required')
        if 'input_assemblySet_ref_B' not in params:
            raise ValueError('input_assemblySet_ref_B parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced AssemblySet'

        # establish workspace client
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)


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
            try:
                #objects = wsClient.get_objects([{'ref': input_assemblySet_ref}])
                objects = wsClient.get_objects2({'objects': [{'ref': input_assemblySet_refs[set_id]}]})['data']
                data = objects[0]['data']
                info = objects[0]['info']
                this_assemblySet = data
                this_assemblySet_obj_name = info[NAME_I]
                input_assemblySet_names[set_id] = this_assemblySet_obj_name;
                type_name = info[TYPE_I].split('.')[1].split('-')[0]
            except Exception as e:
                raise ValueError('Unable to fetch input_assemblySet_ref '+str(input_assemblySet_refs[set_id])+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()
            if type_name != 'AssemblySet':
                raise ValueError("Bad Type:  Should be AssemblySet instead of '" + type_name + "'")

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
                else:  # get standardized genome_ref
                    try:
                        assembly_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_assembly_ref}]})[0]
                        assembly_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", assembly_obj_info[TYPE_I])  # remove trailing version
                    except Exception as e:
                        raise ValueError('Unable to get assembly object info from workspace: (' + str(this_assembly_ref) +')' + str(e))

                    acceptable_types = ["KBaseGenomeAnnotations.Assembly"]
                    if assembly_obj_type not in acceptable_types:
                        raise ValueError("Input Assembly of type: '" + assembly_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))

                    #standardized_assembly_ref = '{}/{}/{}'.format(assembly_obj_info[WSID_I],
                    #                                              assembly_obj_info[OBJID_I],
                    #                                              assembly_obj_info[VERSION_I])
                    standardized_assembly_ref_noVer = '{}/{}'.format(assembly_obj_info[WSID_I],
                                                                     assembly_obj_info[OBJID_I])
                    assembly_ref_to_standardized[this_assembly_ref] = standardized_assembly_ref_noVer
                standardized_assembly_refs.append(standardized_assembly_ref_noVer)  # standardize list
                assembly_obj_present[set_id][standardized_assembly_ref_noVer] = True
                new_items.append({'ref':standardized_assembly_ref_noVer,'label':item['label']})
                self.log(console,"Set {} contains {}".format(set_id,standardized_assembly_ref_noVer))  # DEBUG
            AssemblySet[set_id]['items'] = new_items


        # Build sliced AssemblySet
        #
        self.log (console, "BUILDING SLICED ASSEMBLYSET")  # DEBUG
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
            self.log (console, 'checking assembly {} from set {}'.format(item['ref'],fwd_set_id))  # DEBUG
            this_standardized_assembly_ref_noVer = item['ref']
            if params['operator'] == 'yesA_yesB':
                if assembly_obj_present[rev_set_id].get(this_standardized_assembly_ref_noVer):
                    self.log(console, "keeping assembly {}".format(item['ref']))  # DEBUG
                    output_items.append(item)
            else:
                if not assembly_obj_present[rev_set_id].get(this_standardized_assembly_ref_noVer):
                    self.log(console, "keeping assembly {}".format(item['ref']))  # DEBUG
                    output_items.append(item)
        logMsg = 'assemblies in sliced output set: {}'.format(len(output_items))
        self.log(console, logMsg)


        # Save output AssemblySet
        #
        objects_created = []
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(input_assemblySet_refs['A'])
        provenance[0]['input_ws_objects'].append(input_assemblySet_refs['B'])
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Logical_Slice_Two_AssemblySets'

        if len(output_items) == 0:
            report += 'no assemblies to output under operator '+params['operator']+"\n"
        else:
            # load the method provenance from the context object
            self.log(console, "SETTING PROVENANCE")  # DEBUG

            # Store output Set object
            try:
                setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
            except Exception as e:
                raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))

            if params.get('desc'):
                output_desc = params['desc']
            else:
                output_desc = 'Venn slice '+params['operator']+' of AssemblySets '+input_assemblySet_names['A']+' and '+input_assemblySet_names['B']
            output_assemblySet_obj = { 'description': output_desc,
                                       'items': output_items
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
        self.log(console, "BUILDING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_logical_slice_two_assemblysets_report_' + str(uuid.uuid4())
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


        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'operator' not in params:
            raise ValueError('operator parameter is required')
        if 'input_genomeSet_ref_A' not in params:
            raise ValueError('input_genomeSet_ref_A parameter is required')
        if 'input_genomeSet_ref_B' not in params:
            raise ValueError('input_genomeSet_ref_B parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Sliced GenomeSet'

        # establish workspace client
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)


        # Get GenomeSets
        #
        GenomeSet_element_refs = dict()
        input_genomeSet_refs = dict()
        input_genomeSet_refs['A'] = params['input_genomeSet_ref_A']
        input_genomeSet_refs['B'] = params['input_genomeSet_ref_B']
        input_genomeSet_names = dict()
        for set_id in ['A','B']:
            try:
                #objects = wsClient.get_objects([{'ref': input_genomeSet_ref}])
                objects = wsClient.get_objects2({'objects': [{'ref': input_genomeSet_refs[set_id]}]})['data']
                data = objects[0]['data']
                info = objects[0]['info']
                this_genomeSet = data
                this_genomeSet_obj_name = info[NAME_I]
                input_genomeSet_names[set_id] = this_genomeSet_obj_name;
                type_name = info[TYPE_I].split('.')[1].split('-')[0]
            except Exception as e:
                raise ValueError('Unable to fetch input_genomeSet_ref '+str(input_genomeSet_refs[set_id])+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()
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
                    try:
                        genome_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':this_genome_ref}]})[0]
                        genome_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", genome_obj_info[TYPE_I])  # remove trailing version
                    except Exception as e:
                        raise ValueError('Unable to get genome object info from workspace: (' + str(this_genome_ref) +')' + str(e))

                    acceptable_types = ["KBaseGenomes.Genome","KBaseGenomeAnnotations.GenomeAnnotation"]
                    if genome_obj_type not in acceptable_types:
                        raise ValueError("Input Genome of type: '" + genome_obj_type +
                                         "'.  Must be one of " + ", ".join(acceptable_types))

                    #standardized_genome_ref = '{}/{}/{}'.format(genome_obj_info[WSID_I],
                    #                                            genome_obj_info[OBJID_I],
                    #                                            genome_obj_info[VERSION_I])
                    standardized_genome_ref_noVer = '{}/{}'.format(genome_obj_info[WSID_I],
                                                                   genome_obj_info[OBJID_I])
                    genome_ref_to_standardized[this_genome_ref] = standardized_genome_ref_noVer
                standardized_genome_refs.append(standardized_genome_ref_noVer)  # standardize list
                genome_obj_present[set_id][standardized_genome_ref_noVer] = True
                new_element_refs.append(standardized_genome_ref_noVer)
                self.log(console,"Set {} contains {}".format(set_id,standardized_genome_ref_noVer))  # DEBUG
            GenomeSet_element_refs[set_id] = new_element_refs


        # Build sliced GenomeSet
        #
        self.log (console, "BUILDING SLICED GENOMESET")  # DEBUG
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
            self.log (console, 'checking set {} genome {}'.format(set_id,this_standardized_genome_ref_noVer))  # DEBUG
            if params['operator'] == 'yesA_yesB':
                if genome_obj_present[rev_set_id].get(this_standardized_genome_ref_noVer):
                    output_items.append(this_standardized_genome_ref_noVer)
                    self.log(console, "keeping genome {}".format(this_standardized_genome_ref_noVer))  # DEBUG
            else:
                if not genome_obj_present[rev_set_id].get(this_standardized_genome_ref_noVer):
                    output_items.append(this_standardized_genome_ref_noVer)
                    self.log(console, "keeping genome {}".format(this_standardized_genome_ref_noVer))  # DEBUG
        logMsg = 'genomes in sliced output set: {}'.format(len(output_items))
        self.log(console, logMsg)


        # Save output GenomeSet
        #
        objects_created = []

        # load the method provenance from the context object
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(input_genomeSet_refs['A'])
        provenance[0]['input_ws_objects'].append(input_genomeSet_refs['B'])
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Logical_Slice_Two_GenomeSets'

        if len(output_items) == 0:
            report += 'no genomes to output under operator '+params['operator']+"\n"
        else:
            """
            # Store output Set object (use when we switch over to KBaseSets.GenomeSet)
            try:
                setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
            except Exception as e:
                raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))
            """
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

            """
            try:
                output_assemblySet_ref = setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                        'output_object_name': output_assemblySet_name,
                                                                        'data': output_assemblySet_obj
                                                                        })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))
            """
            new_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                  'objects': [{
                                                      'type': 'KBaseSearch.GenomeSet',
                                                      'data': output_genomeSet_obj,
                                                      'name': output_genomeSet_name,
                                                      'meta': {},
                                                      'provenance': provenance}]})[0]

            objects_created.append({'ref': params['workspace_name'] + '/' + output_genomeSet_name,
                                    'description': output_desc})

            

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_logical_slice_two_genomesets_report_' + str(uuid.uuid4())
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
#        report = 'Running KButil_Merge_GenomeSets with params='
#        report += "\n"+pformat(params)

        #### do some basic checks
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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
                raise ValueError('Unable to fetch input_genomeset_ref '+input_genomeset_ref+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            for gId in list(genomeSet['elements'].keys()):
                old_genomeRef = genomeSet['elements'][gId]['ref']
                this_obj_info = ws.get_object_info_new({'objects':[{'ref':old_genomeRef}]})[0]
                standardized_genomeRef = str(this_obj_info[WORKSPACE_I])+'/'+str(this_obj_info[OBJID_I])
                new_gId = standardized_genomeRef
                if not elements.get(new_gId):
                    elements[new_gId] = dict()
                    elements[new_gId]['ref'] = standardized_genomeRef  # the key line
                    self.log(console, "adding element " + new_gId + " : " + standardized_genomeRef)  # DEBUG

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
                                            })[0]

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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
                    raise ValueError('Unable to fetch genomeRef '+genomeRef+' object from workspace: ' + str(e))
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
                if genomeRef not in list(elements.keys()):
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
                                                         'provenance': provenance}]})[0]

        # build output report object
        #
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        if 'input_ref' not in params:
            raise ValueError('input_ref parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Built GenomeSet'

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
            raise ValueError('Unable to fetch input_ref '+params['input_ref']+' object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()
        if type_name != 'FeatureSet':
            raise ValueError("Bad Type:  Should be FeatureSet instead of '" + type_name + "'")

        # Build GenomeSet
        elements = {}
        genome_seen = dict()

        for fId in list(featureSet['elements'].keys()):
            for genomeRef in featureSet['elements'][fId]:

                if not genome_seen.get(genomeRef):
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
                        errMsg = 'Unable to fetch genomeRef '+genomeRef+' object from workspace: ' + str(e)
                        raise ValueError(errMsg)
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
                                                         'provenance': provenance}]})[0]

        # build output report object
        #
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        if 'input_genome_refs' not in params:
            raise ValueError('input_genome_refs parameter is required')
        if 'input_genomeset_ref' not in params:
            raise ValueError('input_genomeset_ref parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Increased GenomeSet'

        # Build GenomeSet
        elements = dict()
        query_genome_ref_order = []
        
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
                raise ValueError('Unable to fetch input_genomeset_ref '+params['input_genomeset_ref']+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            for gId in list(genomeSet['elements'].keys()):
                genomeRef = genomeSet['elements'][gId]['ref']

                if not elements.get(genomeRef):
                    elements[genomeRef] = dict()
                    elements[genomeRef]['ref'] = genomeRef  # the key line
                    self.log(console, "adding element " + gId + " : " + genomeRef)  # DEBUG

                    query_genome_ref_order.append(genomeRef)
                    

        # add new genomes
        #
        genomeSet_obj_types = ["KBaseSearch.GenomeSet", "KBaseSets.GenomeSet"]
        genome_obj_types    = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.Genome"]
        tree_obj_types      = ["KBaseTrees.Tree"]
        for input_ref in params['input_genome_refs']:
            try:
                query_genome_obj = ws.get_objects2({'objects':[{'ref': input_ref}]})['data'][0]
                query_genome_obj_data = query_genome_obj['data']
                query_genome_obj_info = query_genome_obj['info']
                query_genome_obj_type = query_genome_obj_info[TYPE_I].split('-')[0]
            except:
                raise ValueError("unable to fetch input genome object: " + input_ref)

            # just a genome
            if query_genome_obj_type in genome_obj_types:
                if input_ref not in elements:
                    elements[input_ref] = dict()
                    elements[input_ref]['ref'] = input_ref  # the key line
                    self.log(console, "adding element " + input_ref)  # DEBUG
                    query_genome_ref_order.append(input_ref)

            # handle genomeSet
            elif query_genome_obj_type in genomeSet_obj_types:
                for genome_id in sorted(query_genome_obj_data['elements'].keys()):
                    genome_ref = query_genome_obj_data['elements'][genome_id]['ref']
                    if genome_ref not in elements:
                        elements[genome_ref] = dict()
                        elements[genome_ref]['ref'] = genome_ref  # the key line
                        self.log(console, "adding element " + genome_ref)  # DEBUG
                        query_genome_ref_order.append(genome_ref)

            # handle tree type
            elif query_genome_obj_type in tree_obj_types:
                for genome_id in sorted(query_genome_obj_data['ws_refs'].keys()):
                    genome_ref = query_genome_obj_data['ws_refs'][genome_id]['g'][0]
                    if genome_ref not in elements:
                        elements[genome_ref] = dict()
                        elements[genome_ref]['ref'] = genome_ref  # the key line
                        self.log(console, "adding element " + genome_ref)  # DEBUG
                        query_genome_ref_order.append(genome_ref)
            else:  
                raise ValueError ("bad type for input_genome_refs")


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
                                                'provenance': provenance}]})[0]

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        console = []
        invalid_msgs = []
        self.log(console, 'Running KButil_Remove_Genomes_from_GenomeSet with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
#        report = 'Running KButil_Remove_Genomes_from_GenomeSet with params='
#        report += "\n"+pformat(params)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))  # object_info tuple

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_genomeset_ref' not in params:
            raise ValueError('input_genomeset_ref parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
        if 'desc' not in params:
            params['desc'] = params['output_name']+' Reduced GenomeSet'
        if not params.get('input_genome_refs') and \
           not params.get('nonlocal_genome_names'):
            raise ValueError('must define either Local genomes or Non-local genomes to remove')

            
        # read orig GenomeSet
        #
        genomeSet_workspace = None
        if 'input_genomeset_ref' in params and params['input_genomeset_ref'] is not None:
            try:
                #objects = ws.get_objects([{'ref': params['input_genomeset_ref']}])
                objects = ws.get_objects2(
                    {'objects': [{'ref': params['input_genomeset_ref']}]})['data']
                genomeSet = objects[0]['data']
                info = objects[0]['info']
                genomeSet_workspace = info[WORKSPACE_I]
                
                type_name = info[TYPE_I].split('.')[1].split('-')[0]
                if type_name != 'GenomeSet':
                    raise ValueError("Bad Type: Should be GenomeSet instead of '" + type_name + "'")
            except Exception as e:
                raise ValueError('Unable to fetch input_genomeset_ref '+params['input_genomeset_ref']+' object from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()


        # Build list of genome refs (without version) to skip.
        #  Note: standardize to workspace_name and obj_id
        skip_genomes_by_ref = dict()
        nonlocal_skip_genome_refs = []
        if params.get('input_genome_refs'):
            for genomeRef in params['input_genome_refs']: 
                this_obj_info = ws.get_object_info_new({'objects':[{'ref':genomeRef}]})[0]
                standardized_genomeRef = str(this_obj_info[WORKSPACE_I])+'/'+str(this_obj_info[OBJID_I])
                skip_genomes_by_ref[standardized_genomeRef] = True
        if params.get('nonlocal_genome_names'):
            for gId in list(genomeSet['elements'].keys()):
                genomeRef = genomeSet['elements'][gId]['ref']
                genome_obj_info = ws.get_object_info_new ({'objects':[{'ref':genomeRef}]})[0]
                this_genome_workspace = genome_obj_info[WORKSPACE_I]
                this_genome_objname = genome_obj_info[NAME_I]
                standardized_genomeRef = str(genome_obj_info[WORKSPACE_I])+'/'+str(genome_obj_info[OBJID_I])
                if this_genome_workspace != genomeSet_workspace \
                   and this_genome_objname in params['nonlocal_genome_names']:
                    skip_genomes_by_ref[standardized_genomeRef] = True
                    nonlocal_skip_genome_refs.append(standardized_genomeRef)
                
        # build new genome set without skip genomes
        elements = dict()
        for gId in list(genomeSet['elements'].keys()):
            genomeRef = genomeSet['elements'][gId]['ref']
            this_obj_info = ws.get_object_info_new({'objects':[{'ref':genomeRef}]})[0]
            standardized_genomeRef = str(this_obj_info[WORKSPACE_I])+'/'+str(this_obj_info[OBJID_I])

            # this is where they are removed
            if not skip_genomes_by_ref.get(standardized_genomeRef):
                elements[gId] = dict()
                elements[gId]['ref'] = genomeRef  # the key line
                self.log(console, "keeping element " + gId + " : " + genomeRef)  # DEBUG
            else:
                self.log(console, "removing element " + gId + " : " + genomeRef)  # DEBUG

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
        provenance[0]['input_ws_objects'].extend(nonlocal_skip_genome_refs)
        provenance[0]['service'] = 'kb_SetUtilities'
        provenance[0]['method'] = 'KButil_Remove_Genomes_from_GenomeSet'

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
                                                'provenance': provenance}]})[0]

        # build output report object
        self.log(console, "BUILDING REPORT")  # DEBUG
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

        reportName = 'kb_SetUtilities_remove_genomes_from_genomeset_report_' + str(uuid.uuid4())
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

        #### do some basic checks
        #
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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

        # DEBUG
        #params['input_refs'] = ['18858/2/1', '18858/5/1']

        for libRef in params['input_refs']:

            if not lib_seen.get(libRef):
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

                except Exception as e:
                    raise ValueError('Unable to fetch libRef '+libRef+' object from workspace: ' + str(e))
                if set_type == None:
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
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = list(range(11))

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
        if 'input_refs' not in params:
            raise ValueError('input_refs parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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

        # DEBUG
        #params['input_refs'] = ['18858/2/1', '18858/5/1']

        for assRef in params['input_refs']:

            if not ass_seen.get(assRef):
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
#        report = 'Running KButil_Batch_Create_ReadsSet with params='
#        report += "\n"+pformat(params)


        #### STEP 1: instantiate clients
        ##
        self.log (console, "GETTING WORKSPACE CLIENT")
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)
        self.log (console, "GETTING SetAPI CLIENT")
        try:
            setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
        except Exception as e:
            raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))


        #### STEP 2: do some basic checks
        ##
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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

        # Paired End
        try:
            pe_reads_obj_info_list = wsClient.list_objects(
                {'workspaces': [params['workspace_name']], 'type': "KBaseFile.PairedEndLibrary"})
        except Exception as e:
            raise ValueError ("Unable to list Paired-End Reads objects from workspace: " + params['workspace_name'] + " " + str(e))

        for info in pe_reads_obj_info_list:
            reads_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) +'/' + str(info[VERSION_I])
            reads_name = info[NAME_I]

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' READS_NAME: '"+reads_name+"'")  # DEBUG

            if not name_pattern or regexp_name_pattern.match(reads_name):
                self.log(console, "ADDING "+reads_name+" ("+reads_ref+")")  # DEBUG
                pe_reads_obj_ref_by_name[reads_name] = reads_ref

        # Single End
        try:
            se_reads_obj_info_list = wsClient.list_objects(
                {'workspaces': [params['workspace_name']], 'type': "KBaseFile.SingleEndLibrary"})
        except Exception as e:
            raise ValueError ("Unable to list Single-End Reads objects from workspace: " + params['workspace_name'] + " " + str(e))

        for info in se_reads_obj_info_list:
            reads_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) +'/' + str(info[VERSION_I])
            reads_name = info[NAME_I]

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' READS_NAME: '"+reads_name+"'")  # DEBUG

            if not name_pattern or regexp_name_pattern.match(reads_name):
                self.log(console, "ADDING "+reads_name+" ("+reads_ref+")")  # DEBUG
                se_reads_obj_ref_by_name[reads_name] = reads_ref

        # check for no hits
        if len(list(pe_reads_obj_ref_by_name.keys())) == 0 \
           and len(list(se_reads_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Reads Library objects found")
            else:
                self.log(invalid_msgs, "No Reads Library objects passing name_pattern filter: '"+name_pattern+"'")
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']


        #### STEP 5: Build ReadsSet
        ##
        if len(invalid_msgs) == 0:
            items = []
            reads_ref_list = []

            # pick whether to use single end or paired end hits (favor paired end)
            reads_obj_ref_by_name = dict()
            if len(list(pe_reads_obj_ref_by_name.keys())) == 0 \
               and len(list(se_reads_obj_ref_by_name.keys())) != 0:
                reads_obj_ref_by_name = se_reads_obj_ref_by_name
            else:
                reads_obj_ref_by_name = pe_reads_obj_ref_by_name

            # add readslibs
            for reads_name in sorted (reads_obj_ref_by_name.keys()):
                reads_ref = reads_obj_ref_by_name[reads_name]
                reads_ref_list.append (reads_ref)

                self.log(console,"adding reads library "+reads_name+" : "+reads_ref)  # DEBUG
                items.append ({'ref': reads_ref,
                               'label': reads_name
                               #'data_attachment': ,
                               #'info'
                           })


        #### STEP 6: Store output object
        ##
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING READS_SET")  # DEBUG

            # set provenance
            self.log(console,"SETTING PROVENANCE")  # DEBUG
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']
            # add additional info to provenance here, in this case the input data object reference
            provenance[0]['input_ws_objects'] = []
            for reads_ref in reads_ref_list:
                provenance[0]['input_ws_objects'].append(reads_ref)
            provenance[0]['service'] = 'kb_SetUtilities'
            provenance[0]['method'] = 'KButil_Batch_Create_ReadsSet'

            # object def
            output_readsSet_obj = { 'description': params['desc'],
                                    'items': items
                                }
            output_readsSet_name = params['output_name']
            # object save
            try:
                output_readsSet_ref = setAPI_Client.save_reads_set_v1 ({'workspace_name': params['workspace_name'],
                                                                              'output_object_name': output_readsSet_name,
                                                                              'data': output_readsSet_obj
                                                                          })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save reads library set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        #### STEP 7: build output report object
        ##
        self.log(console,"SAVING REPORT")  # DEBUG
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
        reportName = 'kb_SetUtilities_batch_create_readsset_report_'+str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({
            #'id':info[6],
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


        #### STEP 8: return
        ##
        self.log(console,"BUILDING RETURN OBJECT")
        returnVal = { 'report_name': reportName,
                      'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]),
                      }
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
#        report = 'Running KButil_Batch_Create_AssemblySet with params='
#        report += "\n"+pformat(params)


        #### STEP 1: instantiate clients
        ##
        self.log (console, "GETTING WORKSPACE CLIENT")
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)
        self.log (console, "GETTING SetAPI CLIENT")
        try:
            setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
        except Exception as e:
            raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))


        #### STEP 2: do some basic checks
        ##
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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
        try:
            assembly_obj_info_list = wsClient.list_objects(
                #{'ids': [ws_id], 'type': "KBaseGenomeAnnotations.Assembly"})
                {'workspaces': [params['workspace_name']], 'type': "KBaseGenomeAnnotations.Assembly"})
        except Exception as e:
            raise ValueError("Unable to list Assembly objects from workspace: " + params['workspace_name'] + " " + str(e))

        for info in assembly_obj_info_list:
            assembly_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) +'/' + str(info[VERSION_I])
            assembly_name = info[NAME_I]

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' ASSEMBLY_NAME: '"+assembly_name+"'")  # DEBUG

            if not name_pattern or regexp_name_pattern.match(assembly_name):
                self.log(console, "ADDING "+assembly_name+" ("+assembly_ref+")")  # DEBUG
                assembly_obj_ref_by_name[assembly_name] = assembly_ref

        if len(list(assembly_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Assembly objects found")
            else:
                self.log(invalid_msgs, "No Assembly objects passing name_pattern filter: '"+name_pattern+"'")
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']


        #### STEP 5: Build AssemblySet
        ##
        if len(invalid_msgs) == 0:
            items = []
            assembly_ref_list = []
            for ass_name in sorted (assembly_obj_ref_by_name.keys()):
                # add assembly
                ass_ref = assembly_obj_ref_by_name[ass_name]
                assembly_ref_list.append (ass_ref)

                self.log(console,"adding assembly "+ass_name+" : "+ass_ref)  # DEBUG
                items.append ({'ref': ass_ref,
                               'label': ass_name
                               #'data_attachment': ,
                               #'info'
                           })


        #### STEP 6: Store output object
        ##
        if len(invalid_msgs) == 0:
            self.log(console,"SAVING ASSEMBLY_SET")  # DEBUG

            # set provenance
            self.log(console,"SETTING PROVENANCE")  # DEBUG
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']
            # add additional info to provenance here, in this case the input data object reference
            provenance[0]['input_ws_objects'] = []
            for ass_ref in assembly_ref_list:
                provenance[0]['input_ws_objects'].append(ass_ref)
            provenance[0]['service'] = 'kb_SetUtilities'
            provenance[0]['method'] = 'KButil_Batch_Create_AssemblySet'

            # object def
            output_assemblySet_obj = { 'description': params['desc'],
                                       'items': items
                                   }
            output_assemblySet_name = params['output_name']
            # object save
            try:
                output_assemblySet_ref = setAPI_Client.save_assembly_set_v1 ({'workspace_name': params['workspace_name'],
                                                                              'output_object_name': output_assemblySet_name,
                                                                              'data': output_assemblySet_obj
                                                                          })['set_ref']
            except Exception as e:
                raise ValueError('SetAPI FAILURE: Unable to save assembly set object to workspace: (' + params['workspace_name']+")\n" + str(e))


        #### STEP 7: build output report object
        ##
        self.log(console,"SAVING REPORT")  # DEBUG
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
        reportName = 'kb_SetUtilities_batch_create_assemblyset_report_'+str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({
            #'id':info[6],
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


        #### STEP 8: return
        ##
        self.log(console,"BUILDING RETURN OBJECT")
        returnVal = { 'report_name': reportName,
                      'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]),
                      }
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
#        report = 'Running KButil_Batch_Create_GenomeSet with params='
#        report += "\n"+pformat(params)


        #### STEP 1: instantiate clients
        ##
        self.log (console, "GETTING WORKSPACE CLIENT")
        try:
            wsClient = workspaceService(self.workspaceURL, token=ctx['token'])
        except Exception as e:
            raise ValueError('Unable to connect to workspace at '+self.workspaceURL)+ str(e)
#        self.log (console, "GETTING SetAPI CLIENT")
#        try:
#            setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token'])  # for dynamic service
#        except Exception as e:
#            raise ValueError('ERROR: unable to instantiate SetAPI' + str(e))


        #### STEP 2: do some basic checks
        ##
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'output_name' not in params:
            raise ValueError('output_name parameter is required')
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
        try:
            genome_obj_info_list = wsClient.list_objects(
                #{'ids': [ws_id], 'type': "KBaseGenomeAnnotations.Genome"})
                {'workspaces': [params['workspace_name']], 'type': "KBaseGenomes.Genome"})
        except Exception as e:
            raise ValueError("Unable to list Genome objects from workspace: " + params['workspace_name'] + " " + str(e))

        for info in genome_obj_info_list:
            genome_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) +'/' + str(info[VERSION_I])
            genome_name = info[NAME_I]

            if name_pattern:
                self.log(console, "NAME_PATTERN: '"+name_pattern+"' GENOME_NAME: '"+genome_name+"'")  # DEBUG

            if not name_pattern or regexp_name_pattern.match(genome_name):
                self.log(console, "ADDING "+genome_name+" ("+genome_ref+")")  # DEBUG
                genome_obj_ref_by_name[genome_name] = genome_ref

        if len(list(genome_obj_ref_by_name.keys())) == 0:
            if not name_pattern:
                self.log(invalid_msgs, "No Genome objects found")
            else:
                self.log(invalid_msgs, "No Genome objects passing name_pattern filter: '"+name_pattern+"'")
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']


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

                self.log(console,"adding genome "+gen_name+" : "+gen_ref)  # DEBUG
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
            self.log(console,"SAVING GENOME_SET")  # DEBUG

            # set provenance
            self.log(console,"SETTING PROVENANCE")  # DEBUG
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']
            # add additional info to provenance here, in this case the input data object reference
            provenance[0]['input_ws_objects'] = []
            for ass_ref in genome_ref_list:
                provenance[0]['input_ws_objects'].append(ass_ref)
            provenance[0]['service'] = 'kb_SetUtilities'
            provenance[0]['method'] = 'KButil_Batch_Create_GenomeSet'

            # object def
            output_genomeSet_obj = { 'description': params['desc'],
                                     #'items': items
                                     'elements': elements
                                   }
            output_genomeSet_name = params['output_name']
            # object save
            try:
                #output_genomeSet_ref = setAPI_Client.save_genome_set_v1 ({'workspace_name': params['workspace_name'],
                #                                                          'output_object_name': output_genomeSet_name,
                #                                                          'data': output_genomeSet_obj
                #                                                      })['set_ref']
                new_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
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
        self.log(console,"SAVING REPORT")  # DEBUG
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
        reportName = 'kb_SetUtilities_batch_create_genomeset_report_'+str(uuid.uuid4())
        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        report_obj_info = ws.save_objects({
            #'id':info[6],
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


        #### STEP 8: return
        ##
        self.log(console,"BUILDING RETURN OBJECT")
        returnVal = { 'report_name': reportName,
                      'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]),
                      }
        self.log(console,"KButil_Batch_Create_GenomeSet DONE")
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
