
package us.kbase.kbsetutilities;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: KButil_Batch_Import_Genomes_From_Staging_Params</p>
 * <pre>
 * KButil_Batch_Import_Genomes_From_Staging()
 * **
 * **  Method for importing genomes from staging without explicit naming, creates a GenomeSet
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "desc",
    "staging_folder_path",
    "genome_type",
    "output_name"
})
public class KButilBatchImportGenomesFromStagingParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("desc")
    private String desc;
    @JsonProperty("staging_folder_path")
    private String stagingFolderPath;
    @JsonProperty("genome_type")
    private String genomeType;
    @JsonProperty("output_name")
    private String outputName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public KButilBatchImportGenomesFromStagingParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("desc")
    public String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(String desc) {
        this.desc = desc;
    }

    public KButilBatchImportGenomesFromStagingParams withDesc(String desc) {
        this.desc = desc;
        return this;
    }

    @JsonProperty("staging_folder_path")
    public String getStagingFolderPath() {
        return stagingFolderPath;
    }

    @JsonProperty("staging_folder_path")
    public void setStagingFolderPath(String stagingFolderPath) {
        this.stagingFolderPath = stagingFolderPath;
    }

    public KButilBatchImportGenomesFromStagingParams withStagingFolderPath(String stagingFolderPath) {
        this.stagingFolderPath = stagingFolderPath;
        return this;
    }

    @JsonProperty("genome_type")
    public String getGenomeType() {
        return genomeType;
    }

    @JsonProperty("genome_type")
    public void setGenomeType(String genomeType) {
        this.genomeType = genomeType;
    }

    public KButilBatchImportGenomesFromStagingParams withGenomeType(String genomeType) {
        this.genomeType = genomeType;
        return this;
    }

    @JsonProperty("output_name")
    public String getOutputName() {
        return outputName;
    }

    @JsonProperty("output_name")
    public void setOutputName(String outputName) {
        this.outputName = outputName;
    }

    public KButilBatchImportGenomesFromStagingParams withOutputName(String outputName) {
        this.outputName = outputName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((("KButilBatchImportGenomesFromStagingParams"+" [workspaceName=")+ workspaceName)+", desc=")+ desc)+", stagingFolderPath=")+ stagingFolderPath)+", genomeType=")+ genomeType)+", outputName=")+ outputName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
