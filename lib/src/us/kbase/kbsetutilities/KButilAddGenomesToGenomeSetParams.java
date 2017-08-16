
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
 * <p>Original spec-file type: KButil_Add_Genomes_to_GenomeSet_Params</p>
 * <pre>
 * KButil_Add_Genomes_to_GenomeSet()
 * **
 * **  Method for adding a Genome to a GenomeSet
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_refs",
    "input_genomeset_ref",
    "output_name",
    "desc"
})
public class KButilAddGenomesToGenomeSetParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_refs")
    private String inputGenomeRefs;
    @JsonProperty("input_genomeset_ref")
    private String inputGenomesetRef;
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

    public KButilAddGenomesToGenomeSetParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public KButilAddGenomesToGenomeSetParams withInputGenomeRefs(String inputGenomeRefs) {
        this.inputGenomeRefs = inputGenomeRefs;
        return this;
    }

    @JsonProperty("input_genomeset_ref")
    public String getInputGenomesetRef() {
        return inputGenomesetRef;
    }

    @JsonProperty("input_genomeset_ref")
    public void setInputGenomesetRef(String inputGenomesetRef) {
        this.inputGenomesetRef = inputGenomesetRef;
    }

    public KButilAddGenomesToGenomeSetParams withInputGenomesetRef(String inputGenomesetRef) {
        this.inputGenomesetRef = inputGenomesetRef;
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

    public KButilAddGenomesToGenomeSetParams withOutputName(String outputName) {
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

    public KButilAddGenomesToGenomeSetParams withDesc(String desc) {
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
        return ((((((((((((("KButilAddGenomesToGenomeSetParams"+" [workspaceName=")+ workspaceName)+", inputGenomeRefs=")+ inputGenomeRefs)+", inputGenomesetRef=")+ inputGenomesetRef)+", outputName=")+ outputName)+", desc=")+ desc)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
