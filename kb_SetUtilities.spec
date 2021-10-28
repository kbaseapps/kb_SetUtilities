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


    /* KButil_Localize_GenomeSet()
    **
    **  Method for creating Genome Set with all local Genomes
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;
        data_obj_name  output_name;
    } KButil_Localize_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Localize_GenomeSet_Output;

    funcdef KButil_Localize_GenomeSet (KButil_Localize_GenomeSet_Params params)  returns (KButil_Localize_GenomeSet_Output) authentication required;


    /* KButil_Localize_FeatureSet()
    **
    **  Method for creating Feature Set with all local Genomes
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;
        data_obj_name  output_name;
    } KButil_Localize_FeatureSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Localize_FeatureSet_Output;

    funcdef KButil_Localize_FeatureSet (KButil_Localize_FeatureSet_Params params)  returns (KButil_Localize_FeatureSet_Output) authentication required;


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


    /* KButil_Logical_Slice_Two_FeatureSets()
    **
    **  Method for Slicing Two FeatureSets by Venn overlap
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_featureSet_ref_A;
	data_obj_ref   input_featureSet_ref_B;
	string         operator;
	string         desc;
        data_obj_name  output_name;
    } KButil_Logical_Slice_Two_FeatureSets_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Logical_Slice_Two_FeatureSets_Output;

    funcdef KButil_Logical_Slice_Two_FeatureSets (KButil_Logical_Slice_Two_FeatureSets_Params params)  returns (KButil_Logical_Slice_Two_FeatureSets_Output) authentication required;


    /* KButil_Logical_Slice_Two_AssemblySets()
    **
    **  Method for Slicing Two AssemblySets by Venn overlap
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_assemblySet_ref_A;
	data_obj_ref   input_assemblySet_ref_B;
	string         operator;
	string         desc;
        data_obj_name  output_name;
    } KButil_Logical_Slice_Two_AssemblySets_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Logical_Slice_Two_AssemblySets_Output;

    funcdef KButil_Logical_Slice_Two_AssemblySets (KButil_Logical_Slice_Two_AssemblySets_Params params)  returns (KButil_Logical_Slice_Two_AssemblySets_Output) authentication required;


    /* KButil_Logical_Slice_Two_GenomeSets()
    **
    **  Method for Slicing Two AssemblySets by Venn overlap
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_genomeSet_ref_A;
	data_obj_ref   input_genomeSet_ref_B;
	string         operator;
	string         desc;
        data_obj_name  output_name;
    } KButil_Logical_Slice_Two_GenomeSets_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Logical_Slice_Two_GenomeSets_Output;

    funcdef KButil_Logical_Slice_Two_GenomeSets (KButil_Logical_Slice_Two_GenomeSets_Params params)  returns (KButil_Logical_Slice_Two_GenomeSets_Output) authentication required;


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
	list<data_obj_ref>  input_genome_refs;
        data_obj_ref        input_genomeset_ref;
        data_obj_name       output_name;
	string              desc;
    } KButil_Add_Genomes_to_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Add_Genomes_to_GenomeSet_Output;

    funcdef KButil_Add_Genomes_to_GenomeSet (KButil_Add_Genomes_to_GenomeSet_Params params)  returns (KButil_Add_Genomes_to_GenomeSet_Output) authentication required;


    /* KButil_Remove_Genomes_from_GenomeSet()
    **
    **  Method for removing Genomes from a GenomeSet
    */
    typedef structure {
        workspace_name workspace_name;
	list<data_obj_ref>   input_genome_refs;
	list<data_obj_name>  nonlocal_genome_names;
        data_obj_ref         input_genomeset_ref;
        data_obj_name        output_name;
	string               desc;
    } KButil_Remove_Genomes_from_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Remove_Genomes_from_GenomeSet_Output;

    funcdef KButil_Remove_Genomes_from_GenomeSet (KButil_Remove_Genomes_from_GenomeSet_Params params)  returns (KButil_Remove_Genomes_from_GenomeSet_Output) authentication required;


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


    /* KButil_Batch_Create_ReadsSet()
    **
    **  Method for creating a ReadsSet without specifying individual objects
    */
    typedef structure {
        workspace_name workspace_name;
	string         name_pattern;
        data_obj_name  output_name;
	string         desc;
    } KButil_Batch_Create_ReadsSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Batch_Create_ReadsSet_Output;

    funcdef KButil_Batch_Create_ReadsSet (KButil_Batch_Create_ReadsSet_Params params)  returns (KButil_Batch_Create_ReadsSet_Output) authentication required;


    /* KButil_Batch_Create_AssemblySet()
    **
    **  Method for creating an AssemblySet without specifying individual objects
    */
    typedef structure {
        workspace_name workspace_name;
	string         name_pattern;
        data_obj_name  output_name;
	string         desc;
    } KButil_Batch_Create_AssemblySet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Batch_Create_AssemblySet_Output;

    funcdef KButil_Batch_Create_AssemblySet (KButil_Batch_Create_AssemblySet_Params params)  returns (KButil_Batch_Create_AssemblySet_Output) authentication required;


    /* KButil_Batch_Create_GenomeSet()
    **
    **  Method for creating a GenomeSet without specifying individual objects
    */
    typedef structure {
        workspace_name workspace_name;
	string         name_pattern;
        data_obj_name  output_name;
	string         desc;
    } KButil_Batch_Create_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Batch_Create_GenomeSet_Output;

    funcdef KButil_Batch_Create_GenomeSet (KButil_Batch_Create_GenomeSet_Params params)  returns (KButil_Batch_Create_GenomeSet_Output) authentication required;


    /* KButil_Summarize_GenomeSet()
    **
    **  Method for building an HTML report with Genome summaries
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;
	bool           use_newest_version;
	bool           show_sci_name;
	bool           add_qc;
	bool           add_env_bioelement;
	bool           add_dbCAN;
	bool           checkM_reduced_tree;
    } KButil_Summarize_GenomeSet_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Summarize_GenomeSet_Output;

    funcdef KButil_Summarize_GenomeSet (KButil_Summarize_GenomeSet_Params params)  returns (KButil_Summarize_GenomeSet_Output) authentication required;

};

