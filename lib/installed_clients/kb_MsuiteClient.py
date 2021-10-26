# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except ImportError:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class kb_Msuite(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login',
            service_ver='release',
            async_job_check_time_ms=100, async_job_check_time_scale_percent=150, 
            async_job_check_max_time_ms=300000):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = service_ver
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc,
            async_job_check_time_ms=async_job_check_time_ms,
            async_job_check_time_scale_percent=async_job_check_time_scale_percent,
            async_job_check_max_time_ms=async_job_check_max_time_ms)

    def run_checkM(self, params, context=None):
        """
        :param params: instance of type "CheckMInputParams" (Runs CheckM as a
           command line local function. subcommand - specify the subcommand
           to run; supported options are lineage_wf, tetra, bin_qa_plot,
           dist_plot bin_folder - folder with fasta files representing each
           contig (must end in .fna) out_folder - folder to store output
           plots_folder - folder to save plots to seq_file - the full
           concatenated FASTA file (must end in .fna) of all contigs in your
           bins, used just for running the tetra command tetra_File - specify
           the output/input tetra nucleotide frequency file (generated with
           the tetra command) dist_value - when running dist_plot, set this
           to a value between 0 and 100 threads -  number of threads
           reduced_tree - if set to 1, run checkM with the reduced_tree flag,
           which will keep memory limited to less than 16gb (otherwise needs
           40+ GB, which NJS worker nodes do have) quiet - pass the --quite
           parameter to checkM, but doesn't seem to work for all subcommands)
           -> structure: parameter "subcommand" of String, parameter
           "bin_folder" of String, parameter "out_folder" of String,
           parameter "plots_folder" of String, parameter "seq_file" of
           String, parameter "tetra_file" of String, parameter "dist_value"
           of Long, parameter "threads" of Long, parameter "reduced_tree" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "quiet" of type "boolean" (A boolean - 0 for false,
           1 for true. @range (0, 1))
        """
        return self._client.run_job('kb_Msuite.run_checkM',
                                    [params], self._service_ver, context)

    def run_checkM_lineage_wf(self, params, context=None):
        """
        :param params: instance of type "CheckMLineageWfParams" (input_ref -
           reference to the input Assembly, AssemblySet, Genome, GenomeSet,
           or BinnedContigs data) -> structure: parameter "input_ref" of
           String, parameter "workspace_name" of String, parameter
           "reduced_tree" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "save_output_dir" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "save_plots_dir" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "threads" of Long
        :returns: instance of type "CheckMLineageWfResult" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        return self._client.run_job('kb_Msuite.run_checkM_lineage_wf',
                                    [params], self._service_ver, context)

    def run_checkM_lineage_wf_withFilter(self, params, context=None):
        """
        :param params: instance of type "CheckMLineageWf_withFilter_Params"
           (input_ref - reference to the input BinnedContigs data) ->
           structure: parameter "input_ref" of String, parameter
           "workspace_name" of String, parameter "reduced_tree" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "save_output_dir" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "save_plots_dir" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "completeness_perc" of Double, parameter
           "contamination_perc" of Double, parameter
           "output_filtered_binnedcontigs_obj_name" of String, parameter
           "threads" of Long
        :returns: instance of type "CheckMLineageWf_withFilter_Result" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String, parameter "binned_contig_obj_ref" of type
           "obj_ref" (An X/Y/Z style reference e.g. "WS_ID/OBJ_ID/VER")
        """
        return self._client.run_job('kb_Msuite.run_checkM_lineage_wf_withFilter',
                                    [params], self._service_ver, context)

    def lineage_wf(self, params, context=None):
        """
        A "local method" for calling lineage_wf directly.
        :param params: instance of type "LineageWfParams" (* * Parameters for
           lineage_wf, which runs as a "local method". * * Required
           arguments: *   bin_dir - required - Path to the directory where
           your bins are located *   out_dir - required - Path to a directory
           where we will write output files *   log_path - required - Path to
           a file that will be written to with all log output from *    
           stdout and stderr while running `checkm lineage_wf`. *   options -
           optional - A mapping of options to pass to lineage_wf. See the
           README.md *     in the kb_Msuite repo for a list of all of these.
           For options that have no value, simply *     pass an empty
           string.) -> structure: parameter "bin_dir" of String, parameter
           "out_dir" of String, parameter "log_path" of String, parameter
           "options" of mapping from String to String
        :returns: instance of type "LineageWfResult" (* * Output results of
           running the lineage_wf local method. * This returns nothing. Check
           the contents of log_path and out_dir which were passed as *
           parameters to see the output of running this function.) ->
           structure:
        """
        return self._client.run_job('kb_Msuite.lineage_wf',
                                    [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.run_job('kb_Msuite.status',
                                    [], self._service_ver, context)