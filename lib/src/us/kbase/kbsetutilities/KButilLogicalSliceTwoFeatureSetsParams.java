
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
 * <p>Original spec-file type: KButil_Logical_Slice_Two_FeatureSets_Params</p>
 * <pre>
 * KButil_Logical_Slice_Two_FeatureSets()
 * **
 * **  Method for Slicing Two FeatureSets by Venn overlap
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_featureSet_ref_A",
    "input_featureSet_ref_B",
    "operator",
    "desc",
    "output_name"
})
public class KButilLogicalSliceTwoFeatureSetsParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_featureSet_ref_A")
    private String inputFeatureSetRefA;
    @JsonProperty("input_featureSet_ref_B")
    private String inputFeatureSetRefB;
    @JsonProperty("operator")
    private String operator;
    @JsonProperty("desc")
    private String desc;
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

    public KButilLogicalSliceTwoFeatureSetsParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_featureSet_ref_A")
    public String getInputFeatureSetRefA() {
        return inputFeatureSetRefA;
    }

    @JsonProperty("input_featureSet_ref_A")
    public void setInputFeatureSetRefA(String inputFeatureSetRefA) {
        this.inputFeatureSetRefA = inputFeatureSetRefA;
    }

    public KButilLogicalSliceTwoFeatureSetsParams withInputFeatureSetRefA(String inputFeatureSetRefA) {
        this.inputFeatureSetRefA = inputFeatureSetRefA;
        return this;
    }

    @JsonProperty("input_featureSet_ref_B")
    public String getInputFeatureSetRefB() {
        return inputFeatureSetRefB;
    }

    @JsonProperty("input_featureSet_ref_B")
    public void setInputFeatureSetRefB(String inputFeatureSetRefB) {
        this.inputFeatureSetRefB = inputFeatureSetRefB;
    }

    public KButilLogicalSliceTwoFeatureSetsParams withInputFeatureSetRefB(String inputFeatureSetRefB) {
        this.inputFeatureSetRefB = inputFeatureSetRefB;
        return this;
    }

    @JsonProperty("operator")
    public String getOperator() {
        return operator;
    }

    @JsonProperty("operator")
    public void setOperator(String operator) {
        this.operator = operator;
    }

    public KButilLogicalSliceTwoFeatureSetsParams withOperator(String operator) {
        this.operator = operator;
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

    public KButilLogicalSliceTwoFeatureSetsParams withDesc(String desc) {
        this.desc = desc;
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

    public KButilLogicalSliceTwoFeatureSetsParams withOutputName(String outputName) {
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
        return ((((((((((((((("KButilLogicalSliceTwoFeatureSetsParams"+" [workspaceName=")+ workspaceName)+", inputFeatureSetRefA=")+ inputFeatureSetRefA)+", inputFeatureSetRefB=")+ inputFeatureSetRefB)+", operator=")+ operator)+", desc=")+ desc)+", outputName=")+ outputName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
