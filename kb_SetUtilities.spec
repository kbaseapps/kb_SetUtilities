/*
** A KBase module: kb_SetUtilities
**
** This module contains basic utilities for set manipulation, originally extracted
** from kb_util_dylan
**
*/

module kb_SetUtilities {

    /* 
    ** The workspace object refs are of form:
    **
    **    objects = ws.get_objects([{'ref': params['workspace_id']+'/'+params['obj_name']}])
    **
    ** "ref" means the entire name combining the workspace id and the object name
    ** "id" is a numerical identifier of the workspace or object, and should just be used for workspace
    ** "name" is a string identifier of a workspace or object.  This is received from Narrative.
    */
    typedef string workspace_name;
    typedef string sequence;
    typedef string data_obj_name;
    typedef string data_obj_ref;
    typedef int    bool;


    /* KButil_Merge_FeatureSet_Collection()
    **
    **  Method for merging FeatureSets
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Merge_FeatureSet_Collection_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Merge_FeatureSet_Collection_Output;

    funcdef KButil_Merge_FeatureSet_Collection (KButil_Merge_FeatureSet_Collection_Params params)  returns (KButil_Merge_FeatureSet_Collection_Output) authentication required;


    /* KButil_Slice_FeatureSets_by_Genomes()
    **
    **  Method for Slicing a FeatureSet or FeatureSets by a Genome, Genomes, or GenomeSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_featureSet_refs;
	data_obj_ref   input_genome_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Slice_FeatureSets_by_Genomes_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Slice_FeatureSets_by_Genomes_Output;

    funcdef KButil_Slice_FeatureSets_by_Genomes (KButil_Slice_FeatureSets_by_Genomes_Params params)  returns (KButil_Slice_FeatureSets_by_Genomes_Output) authentication required;


    /* KButil_Merge_GenomeSets()
    **
    **  Method for merging GenomeSets
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Merge_GenomeSets_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Merge_GenomeSets_Output;

    funcdef KButil_Merge_GenomeSets (KButil_Merge_GenomeSets_Params params)  returns (KButil_Merge_GenomeSets_Output) authentication required;


    /* KButil_Build_GenomeSet()
    **
    **  Method for creating a GenomeSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Build_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Build_GenomeSet_Output;

    funcdef KButil_Build_GenomeSet (KButil_Build_GenomeSet_Params params)  returns (KButil_Build_GenomeSet_Output) authentication required;


    /* KButil_Build_GenomeSet_from_FeatureSet()
    **
    **  Method for obtaining a GenomeSet from a FeatureSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;
        data_obj_name  output_name;
	string         desc;
    } KButil_Build_GenomeSet_from_FeatureSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Build_GenomeSet_from_FeatureSet_Output;

    funcdef KButil_Build_GenomeSet_from_FeatureSet (KButil_Build_GenomeSet_from_FeatureSet_Params params)  returns (KButil_Build_GenomeSet_from_FeatureSet_Output) authentication required;


    /* KButil_Add_Genomes_to_GenomeSet()
    **
    **  Method for adding a Genome to a GenomeSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_genome_refs;
        data_obj_ref   input_genomeset_ref;
        data_obj_name  output_name;
	string         desc;
    } KButil_Add_Genomes_to_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Add_Genomes_to_GenomeSet_Output;

    funcdef KButil_Add_Genomes_to_GenomeSet (KButil_Add_Genomes_to_GenomeSet_Params params)  returns (KButil_Add_Genomes_to_GenomeSet_Output) authentication required;


    /* KButil_Build_ReadsSet()
    **
    **  Method for creating a ReadsSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Build_ReadsSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Build_ReadsSet_Output;

    funcdef KButil_Build_ReadsSet (KButil_Build_ReadsSet_Params params)  returns (KButil_Build_ReadsSet_Output) authentication required;


    /* KButil_Merge_MultipleReadsSets_to_OneReadsSet()
    **
    **  Method for merging multiple ReadsSets into one ReadsSet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;    /* ReadsSets */
        data_obj_name  output_name;   /* ReadsSet */
	string         desc;
    } KButil_Merge_MultipleReadsSets_to_OneReadsSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Merge_MultipleReadsSets_to_OneReadsSet_Output;

    funcdef KButil_Merge_MultipleReadsSets_to_OneReadsSet (KButil_Merge_MultipleReadsSets_to_OneReadsSet_Params params)  returns (KButil_Merge_MultipleReadsSets_to_OneReadsSet_Output) authentication required;


    /* KButil_Build_AssemblySet()
    **
    **  Method for creating an AssemblySet
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
    } KButil_Build_AssemblySet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Build_AssemblySet_Output;

    funcdef KButil_Build_AssemblySet (KButil_Build_AssemblySet_Params params)  returns (KButil_Build_AssemblySet_Output) authentication required;

};

