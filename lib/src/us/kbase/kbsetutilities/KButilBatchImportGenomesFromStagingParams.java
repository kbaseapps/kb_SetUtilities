
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
    "output_name",
    "source",
    "taxon_wsname",
    "taxon_reference",
    "release",
    "genetic_code",
    "generate_missing_genes"
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
    @JsonProperty("source")
    private String source;
    @JsonProperty("taxon_wsname")
    private String taxonWsname;
    @JsonProperty("taxon_reference")
    private String taxonReference;
    @JsonProperty("release")
    private String release;
    @JsonProperty("genetic_code")
    private Long geneticCode;
    @JsonProperty("generate_missing_genes")
    private Long generateMissingGenes;
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

    @JsonProperty("source")
    public String getSource() {
        return source;
    }

    @JsonProperty("source")
    public void setSource(String source) {
        this.source = source;
    }

    public KButilBatchImportGenomesFromStagingParams withSource(String source) {
        this.source = source;
        return this;
    }

    @JsonProperty("taxon_wsname")
    public String getTaxonWsname() {
        return taxonWsname;
    }

    @JsonProperty("taxon_wsname")
    public void setTaxonWsname(String taxonWsname) {
        this.taxonWsname = taxonWsname;
    }

    public KButilBatchImportGenomesFromStagingParams withTaxonWsname(String taxonWsname) {
        this.taxonWsname = taxonWsname;
        return this;
    }

    @JsonProperty("taxon_reference")
    public String getTaxonReference() {
        return taxonReference;
    }

    @JsonProperty("taxon_reference")
    public void setTaxonReference(String taxonReference) {
        this.taxonReference = taxonReference;
    }

    public KButilBatchImportGenomesFromStagingParams withTaxonReference(String taxonReference) {
        this.taxonReference = taxonReference;
        return this;
    }

    @JsonProperty("release")
    public String getRelease() {
        return release;
    }

    @JsonProperty("release")
    public void setRelease(String release) {
        this.release = release;
    }

    public KButilBatchImportGenomesFromStagingParams withRelease(String release) {
        this.release = release;
        return this;
    }

    @JsonProperty("genetic_code")
    public Long getGeneticCode() {
        return geneticCode;
    }

    @JsonProperty("genetic_code")
    public void setGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
    }

    public KButilBatchImportGenomesFromStagingParams withGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
        return this;
    }

    @JsonProperty("generate_missing_genes")
    public Long getGenerateMissingGenes() {
        return generateMissingGenes;
    }

    @JsonProperty("generate_missing_genes")
    public void setGenerateMissingGenes(Long generateMissingGenes) {
        this.generateMissingGenes = generateMissingGenes;
    }

    public KButilBatchImportGenomesFromStagingParams withGenerateMissingGenes(Long generateMissingGenes) {
        this.generateMissingGenes = generateMissingGenes;
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
        return ((((((((((((((((((((((((("KButilBatchImportGenomesFromStagingParams"+" [workspaceName=")+ workspaceName)+", desc=")+ desc)+", stagingFolderPath=")+ stagingFolderPath)+", genomeType=")+ genomeType)+", outputName=")+ outputName)+", source=")+ source)+", taxonWsname=")+ taxonWsname)+", taxonReference=")+ taxonReference)+", release=")+ release)+", geneticCode=")+ geneticCode)+", generateMissingGenes=")+ generateMissingGenes)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
