package us.kbase.kbsetutilities;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: kb_SetUtilities</p>
 * <pre>
 * ** A KBase module: kb_SetUtilities
 * **
 * ** This module contains basic utilities for set manipulation, originally extracted
 * ** from kb_util_dylan
 * **
 * </pre>
 */
public class KbSetUtilitiesClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public KbSetUtilitiesClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public KbSetUtilitiesClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbSetUtilitiesClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbSetUtilitiesClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: KButil_Localize_GenomeSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilLocalizeGenomeSetParams KButilLocalizeGenomeSetParams} (original type "KButil_Localize_GenomeSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilLocalizeGenomeSetOutput KButilLocalizeGenomeSetOutput} (original type "KButil_Localize_GenomeSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilLocalizeGenomeSetOutput kButilLocalizeGenomeSet(KButilLocalizeGenomeSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilLocalizeGenomeSetOutput>> retType = new TypeReference<List<KButilLocalizeGenomeSetOutput>>() {};
        List<KButilLocalizeGenomeSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Localize_GenomeSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Localize_FeatureSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilLocalizeFeatureSetParams KButilLocalizeFeatureSetParams} (original type "KButil_Localize_FeatureSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilLocalizeFeatureSetOutput KButilLocalizeFeatureSetOutput} (original type "KButil_Localize_FeatureSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilLocalizeFeatureSetOutput kButilLocalizeFeatureSet(KButilLocalizeFeatureSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilLocalizeFeatureSetOutput>> retType = new TypeReference<List<KButilLocalizeFeatureSetOutput>>() {};
        List<KButilLocalizeFeatureSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Localize_FeatureSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Merge_FeatureSet_Collection</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilMergeFeatureSetCollectionParams KButilMergeFeatureSetCollectionParams} (original type "KButil_Merge_FeatureSet_Collection_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilMergeFeatureSetCollectionOutput KButilMergeFeatureSetCollectionOutput} (original type "KButil_Merge_FeatureSet_Collection_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilMergeFeatureSetCollectionOutput kButilMergeFeatureSetCollection(KButilMergeFeatureSetCollectionParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilMergeFeatureSetCollectionOutput>> retType = new TypeReference<List<KButilMergeFeatureSetCollectionOutput>>() {};
        List<KButilMergeFeatureSetCollectionOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Merge_FeatureSet_Collection", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Slice_FeatureSets_by_Genomes</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilSliceFeatureSetsByGenomesParams KButilSliceFeatureSetsByGenomesParams} (original type "KButil_Slice_FeatureSets_by_Genomes_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilSliceFeatureSetsByGenomesOutput KButilSliceFeatureSetsByGenomesOutput} (original type "KButil_Slice_FeatureSets_by_Genomes_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilSliceFeatureSetsByGenomesOutput kButilSliceFeatureSetsByGenomes(KButilSliceFeatureSetsByGenomesParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilSliceFeatureSetsByGenomesOutput>> retType = new TypeReference<List<KButilSliceFeatureSetsByGenomesOutput>>() {};
        List<KButilSliceFeatureSetsByGenomesOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Slice_FeatureSets_by_Genomes", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Logical_Slice_Two_FeatureSets</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilLogicalSliceTwoFeatureSetsParams KButilLogicalSliceTwoFeatureSetsParams} (original type "KButil_Logical_Slice_Two_FeatureSets_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilLogicalSliceTwoFeatureSetsOutput KButilLogicalSliceTwoFeatureSetsOutput} (original type "KButil_Logical_Slice_Two_FeatureSets_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilLogicalSliceTwoFeatureSetsOutput kButilLogicalSliceTwoFeatureSets(KButilLogicalSliceTwoFeatureSetsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilLogicalSliceTwoFeatureSetsOutput>> retType = new TypeReference<List<KButilLogicalSliceTwoFeatureSetsOutput>>() {};
        List<KButilLogicalSliceTwoFeatureSetsOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Logical_Slice_Two_FeatureSets", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Merge_GenomeSets</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilMergeGenomeSetsParams KButilMergeGenomeSetsParams} (original type "KButil_Merge_GenomeSets_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilMergeGenomeSetsOutput KButilMergeGenomeSetsOutput} (original type "KButil_Merge_GenomeSets_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilMergeGenomeSetsOutput kButilMergeGenomeSets(KButilMergeGenomeSetsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilMergeGenomeSetsOutput>> retType = new TypeReference<List<KButilMergeGenomeSetsOutput>>() {};
        List<KButilMergeGenomeSetsOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Merge_GenomeSets", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Build_GenomeSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBuildGenomeSetParams KButilBuildGenomeSetParams} (original type "KButil_Build_GenomeSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBuildGenomeSetOutput KButilBuildGenomeSetOutput} (original type "KButil_Build_GenomeSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBuildGenomeSetOutput kButilBuildGenomeSet(KButilBuildGenomeSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBuildGenomeSetOutput>> retType = new TypeReference<List<KButilBuildGenomeSetOutput>>() {};
        List<KButilBuildGenomeSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Build_GenomeSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Build_GenomeSet_from_FeatureSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBuildGenomeSetFromFeatureSetParams KButilBuildGenomeSetFromFeatureSetParams} (original type "KButil_Build_GenomeSet_from_FeatureSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBuildGenomeSetFromFeatureSetOutput KButilBuildGenomeSetFromFeatureSetOutput} (original type "KButil_Build_GenomeSet_from_FeatureSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBuildGenomeSetFromFeatureSetOutput kButilBuildGenomeSetFromFeatureSet(KButilBuildGenomeSetFromFeatureSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBuildGenomeSetFromFeatureSetOutput>> retType = new TypeReference<List<KButilBuildGenomeSetFromFeatureSetOutput>>() {};
        List<KButilBuildGenomeSetFromFeatureSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Build_GenomeSet_from_FeatureSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Add_Genomes_to_GenomeSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilAddGenomesToGenomeSetParams KButilAddGenomesToGenomeSetParams} (original type "KButil_Add_Genomes_to_GenomeSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilAddGenomesToGenomeSetOutput KButilAddGenomesToGenomeSetOutput} (original type "KButil_Add_Genomes_to_GenomeSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilAddGenomesToGenomeSetOutput kButilAddGenomesToGenomeSet(KButilAddGenomesToGenomeSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilAddGenomesToGenomeSetOutput>> retType = new TypeReference<List<KButilAddGenomesToGenomeSetOutput>>() {};
        List<KButilAddGenomesToGenomeSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Add_Genomes_to_GenomeSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Build_ReadsSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBuildReadsSetParams KButilBuildReadsSetParams} (original type "KButil_Build_ReadsSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBuildReadsSetOutput KButilBuildReadsSetOutput} (original type "KButil_Build_ReadsSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBuildReadsSetOutput kButilBuildReadsSet(KButilBuildReadsSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBuildReadsSetOutput>> retType = new TypeReference<List<KButilBuildReadsSetOutput>>() {};
        List<KButilBuildReadsSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Build_ReadsSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Merge_MultipleReadsSets_to_OneReadsSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilMergeMultipleReadsSetsToOneReadsSetParams KButilMergeMultipleReadsSetsToOneReadsSetParams} (original type "KButil_Merge_MultipleReadsSets_to_OneReadsSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilMergeMultipleReadsSetsToOneReadsSetOutput KButilMergeMultipleReadsSetsToOneReadsSetOutput} (original type "KButil_Merge_MultipleReadsSets_to_OneReadsSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilMergeMultipleReadsSetsToOneReadsSetOutput kButilMergeMultipleReadsSetsToOneReadsSet(KButilMergeMultipleReadsSetsToOneReadsSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilMergeMultipleReadsSetsToOneReadsSetOutput>> retType = new TypeReference<List<KButilMergeMultipleReadsSetsToOneReadsSetOutput>>() {};
        List<KButilMergeMultipleReadsSetsToOneReadsSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Merge_MultipleReadsSets_to_OneReadsSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Build_AssemblySet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBuildAssemblySetParams KButilBuildAssemblySetParams} (original type "KButil_Build_AssemblySet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBuildAssemblySetOutput KButilBuildAssemblySetOutput} (original type "KButil_Build_AssemblySet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBuildAssemblySetOutput kButilBuildAssemblySet(KButilBuildAssemblySetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBuildAssemblySetOutput>> retType = new TypeReference<List<KButilBuildAssemblySetOutput>>() {};
        List<KButilBuildAssemblySetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Build_AssemblySet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Batch_Create_AssemblySet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBatchCreateAssemblySetParams KButilBatchCreateAssemblySetParams} (original type "KButil_Batch_Create_AssemblySet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBatchCreateAssemblySetOutput KButilBatchCreateAssemblySetOutput} (original type "KButil_Batch_Create_AssemblySet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBatchCreateAssemblySetOutput kButilBatchCreateAssemblySet(KButilBatchCreateAssemblySetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBatchCreateAssemblySetOutput>> retType = new TypeReference<List<KButilBatchCreateAssemblySetOutput>>() {};
        List<KButilBatchCreateAssemblySetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Batch_Create_AssemblySet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: KButil_Batch_Create_GenomeSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbsetutilities.KButilBatchCreateGenomeSetParams KButilBatchCreateGenomeSetParams} (original type "KButil_Batch_Create_GenomeSet_Params")
     * @return   instance of type {@link us.kbase.kbsetutilities.KButilBatchCreateGenomeSetOutput KButilBatchCreateGenomeSetOutput} (original type "KButil_Batch_Create_GenomeSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public KButilBatchCreateGenomeSetOutput kButilBatchCreateGenomeSet(KButilBatchCreateGenomeSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<KButilBatchCreateGenomeSetOutput>> retType = new TypeReference<List<KButilBatchCreateGenomeSetOutput>>() {};
        List<KButilBatchCreateGenomeSetOutput> res = caller.jsonrpcCall("kb_SetUtilities.KButil_Batch_Create_GenomeSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("kb_SetUtilities.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
