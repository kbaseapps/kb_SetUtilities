### Version 1.9.0
__Changes__
- Added "Split GenomeSet" App

### Version 1.8.0
__Changes__
- Added "Summarize Genome Set" App
- Added GenomeSet as valid filter to Slice FeatureSets by Genomes()

### Version 1.7.6
__Changes__
- fixed bugs found in narrative beta testing
- added error when trying to build ReadsSet mixing PE and SE
- removed redundant output cells from Set creation Apps
- made set_provenance() method
- updated to use KBaseReport.create()
- followed recommended code tidying

### Version 1.7.5
__Changes__
- added Github Actions unit testing
- tidied up links to support in App Docs

### Version 1.7.4
__Changes__
- added support for FeatureSets that may include Annotated Metagenome Assembly features to
  * KButil_Merge_FeatureSet_Collection
- fixed bug in KButil_Merge_FeatureSet_Collection to avoid duplication
- fixed bug in KButil_Logical_Slice_*() that was returning union for yesA_notB and notA_yesB
- updated path to support URL

### Version 1.7.3
__Changes__
- fixed bug in "Merge GenomeSets" caused by SpeciesTree GenomeSet elements having same ids

### Version 1.7.2
__Changes__
- added GenomeSets and SpeciesTrees as option to be added in "Add Genomes to GenomeSet"

### Version 1.7.1
__Changes__
- tweaked Venn Slice to fix bug in GenomeSet and improve icon

### Version 1.7.0
__Changes__
- added support for FeatureSets that may include Annotated Metagenome Assembly features to
  * KButil_Slice_FeatureSets_by_Genomes
  * KButil_Build_GenomeSet_from_FeatureSet
  * KButil_Logical_Slice_Two_FeatureSets (aka "Venn Slice")

### Version 1.6.0
__Changes__
- added "Venn Slice Two AssemblySets" App
- added "Venn Slice Two GenomeSets" App

### Version 1.5.0
__Changes__
- added KButil_Remove_Genomes_from_GenomeSet()
- changed KButil_Add_Genomes_to_GenomeSet() to accept genome object list
- Description input field no longer required in Apps

### Version 1.4.0
__Changes__
- added KButil_Batch_Create_ReadsSet()

### Version 1.3.0
__Changes__
- update to python3

### Version 1.2.0
__Changes__
- added KButil_Batch_Create_GenomeSet()
- added KButil_Batch_Create_AssemblySet()

### Version 1.1.3
__Changes__
- added unit test data

### Version 1.1.2
__Changes__
- added KBase paper citation in PLOS format 

### Version 1.1.1
__Changes__
- updated base docker image to sdkbase2
- improved docs pages for Apps

### Version 1.1.0
__Changes__
- added "Slice FeatureSets by Genomes" App
- added "Logical Slice Two FeatureSets" App
- added transformation diagrams to docs pages

### Version 1.0.1
__Changes__
- changed contact from email to url

### Version 1.0.0
- Initial release
