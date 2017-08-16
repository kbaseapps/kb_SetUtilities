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


    /* KButil_Insert_SingleEndLibrary()
    **
    ** Method for Inserting a textarea field with FASTA or FASTQ into a SingleEndLibrary object and importing into SHOCK and WS
    */
    /*
    typedef structure {
        workspace_name workspace_name;
	sequence       input_sequence;
        data_obj_name  output_name;
    } KButil_Insert_SingleEndLibrary_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    */
/*       data_obj_ref  output_filtered_ref;
*
*        int n_initial_seqs;
*        int n_seqs_matched;
*        int n_seqs_notmatched;
*/
    /*
    } KButil_Insert_SingleEndLibrary_Output;
    */
    /*funcdef KButil_Insert_SingleEndLibrary (KButil_Insert_SingleEndLibrary_Params params)  returns (KButil_Insert_SingleEndLibrary_Output) authentication required;
    */
	

    /* KButil_FASTQ_to_FASTA()
    **
    ** Method for Converting a FASTQ SingleEndLibrary to a FASTA SingleEndLibrary
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;
        data_obj_name  output_name;
    } KButil_FASTQ_to_FASTA_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
/*       data_obj_ref  output_filtered_ref;
*
*        int n_initial_seqs;
*        int n_seqs_matched;
*        int n_seqs_notmatched;
*/
    } KButil_FASTQ_to_FASTA_Output;
	
    funcdef KButil_FASTQ_to_FASTA (KButil_FASTQ_to_FASTA_Params params)  returns (KButil_FASTQ_to_FASTA_Output) authentication required;


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


    /* KButil_Concat_MSAs()
    **
    **  Method for Concatenating MSAs into a combined MSA
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;
        data_obj_name  output_name;
	string         desc;
	bool           blanks_flag;
    } KButil_Concat_MSAs_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Concat_MSAs_Output;

    funcdef KButil_Concat_MSAs (KButil_Concat_MSAs_Params params)  returns (KButil_Concat_MSAs_Output) authentication required;


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


    /* KButil_Split_Reads()
    **
    **  Method for spliting a ReadsLibrary into evenly sized ReadsLibraries
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;    /* ReadsLibrary */
        data_obj_name  output_name;  /* ReadsSet */
	int            split_num;
	string         desc;
    } KButil_Split_Reads_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Split_Reads_Output;

    funcdef KButil_Split_Reads (KButil_Split_Reads_Params params)  returns (KButil_Split_Reads_Output) authentication required;


    /* KButil_Random_Subsample_Reads()
    **
    **  Method for random subsampling of reads library
    */
    typedef structure {
	int            split_num;
	int            reads_num;
	float          reads_perc;
    } Fractionate_Options;
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;    /* ReadsLibrary */
        data_obj_name  output_name;  /* ReadsSet */
	Fractionate_Options subsample_fraction;
	/*bool           reads_uniq;*/  /* sampling without replacement */
	string         desc;
	int            seed;
    } KButil_Random_Subsample_Reads_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Random_Subsample_Reads_Output;

    funcdef KButil_Random_Subsample_Reads (KButil_Random_Subsample_Reads_Params params)  returns (KButil_Random_Subsample_Reads_Output) authentication required;


    /* KButil_Merge_ReadsSet_to_OneLibrary()
    **
    **  Method for merging a ReadsSet into one library
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;    /* ReadsSet */
        data_obj_name  output_name;  /* ReadsLibrary */
	string         desc;
    } KButil_Merge_ReadsSet_to_OneLibrary_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Merge_ReadsSet_to_OneLibrary_Output;

    funcdef KButil_Merge_ReadsSet_to_OneLibrary (KButil_Merge_ReadsSet_to_OneLibrary_Params params)  returns (KButil_Merge_ReadsSet_to_OneLibrary_Output) authentication required;


    /* KButil_Merge_MultipleReadsLibs_to_OneLibrary()
    **
    **  Method for merging ReadsLibs into one library
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;    /* ReadsLibraries */
        data_obj_name  output_name;  /* ReadsLibrary */
	string         desc;
    } KButil_Merge_MultipleReadsLibs_to_OneLibrary_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Merge_MultipleReadsLibs_to_OneLibrary_Output;

    funcdef KButil_Merge_MultipleReadsLibs_to_OneLibrary (KButil_Merge_MultipleReadsLibs_to_OneLibrary_Params params)  returns (KButil_Merge_MultipleReadsLibs_to_OneLibrary_Output) authentication required;


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


    /* KButil_Extract_Unpaired_Reads_and_Synchronize_Pairs()
    **
    **  Method for removing unpaired reads from a paired end library or set and matching the order of reads
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_ref;    /* ReadsSet or ReadLibrary */
        data_obj_name  output_name;  /* ReadsSet or ReadLibrary */
	string         desc;
    } KButil_Extract_Unpaired_Reads_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Extract_Unpaired_Reads_Output;

    funcdef KButil_Extract_Unpaired_Reads_and_Synchronize_Pairs (KButil_Extract_Unpaired_Reads_Params params)  returns (KButil_Extract_Unpaired_Reads_Output) authentication required;


    /* KButil_Translate_ReadsLibs_QualScores()
    **
    **  Method for Translating ReadsLibs Qual scores
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;    /* ReadsLibraries */
    } KButil_Translate_ReadsLibs_QualScores_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_Translate_ReadsLibs_QualScores_Output;

    funcdef KButil_Translate_ReadsLibs_QualScores (KButil_Translate_ReadsLibs_QualScores_Params params)  returns (KButil_Translate_ReadsLibs_QualScores_Output) authentication required;


    /* KButil_AddInsertLen_to_ReadsLibs()
    **
    **  Method for Adding Insert Len to PairedEnd ReadsLibs
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_refs;    /* ReadsLibraries */
	float          insert_len;
	float          insert_stddev;
    } KButil_AddInsertLen_to_ReadsLibs_Params;

    typedef structure {
	data_obj_name report_name;
	data_obj_ref  report_ref;
    } KButil_AddInsertLen_to_ReadsLibs_Output;

    funcdef KButil_AddInsertLen_to_ReadsLibs (KButil_AddInsertLen_to_ReadsLibs_Params params)  returns (KButil_AddInsertLen_to_ReadsLibs_Output) authentication required;


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

