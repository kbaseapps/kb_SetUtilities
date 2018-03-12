
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
 * <p>Original spec-file type: KButil_Slice_FeatureSets_by_Genomes_Params</p>
 * <pre>
 * KButil_Slice_FeatureSets_by_Genomes()
 * **
 * **  Method for Slicing a FeatureSet or FeatureSets by a Genome, Genomes, or GenomeSet
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_featureSet_refs",
    "input_genome_refs",
    "output_name",
    "desc"
})
public class KButilSliceFeatureSetsByGenomesParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_featureSet_refs")
    private String inputFeatureSetRefs;
    @JsonProperty("input_genome_refs")
    private String inputGenomeRefs;
    @JsonProperty("output_name")
    private String outputName;
    @JsonProperty("desc")
    private String desc;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public KButilSliceFeatureSetsByGenomesParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_featureSet_refs")
    public String getInputFeatureSetRefs() {
        return inputFeatureSetRefs;
    }

    @JsonProperty("input_featureSet_refs")
    public void setInputFeatureSetRefs(String inputFeatureSetRefs) {
        this.inputFeatureSetRefs = inputFeatureSetRefs;
    }

    public KButilSliceFeatureSetsByGenomesParams withInputFeatureSetRefs(String inputFeatureSetRefs) {
        this.inputFeatureSetRefs = inputFeatureSetRefs;
        return this;
    }

    @JsonProperty("input_genome_refs")
    public String getInputGenomeRefs() {
        return inputGenomeRefs;
    }

    @JsonProperty("input_genome_refs")
    public void setInputGenomeRefs(String inputGenomeRefs) {
        this.inputGenomeRefs = inputGenomeRefs;
    }

    public KButilSliceFeatureSetsByGenomesParams withInputGenomeRefs(String inputGenomeRefs) {
        this.inputGenomeRefs = inputGenomeRefs;
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

    public KButilSliceFeatureSetsByGenomesParams withOutputName(String outputName) {
        this.outputName = outputName;
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

    public KButilSliceFeatureSetsByGenomesParams withDesc(String desc) {
        this.desc = desc;
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
        return ((((((((((((("KButilSliceFeatureSetsByGenomesParams"+" [workspaceName=")+ workspaceName)+", inputFeatureSetRefs=")+ inputFeatureSetRefs)+", inputGenomeRefs=")+ inputGenomeRefs)+", outputName=")+ outputName)+", desc=")+ desc)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
