SOURCE_DIR=kitchensink/kitchensink
OUTDIR=$PWD/analysis_reports/kitchensink
mkdir -p $OUTDIR
time ./bin/kantra analyze -i $PWD/sample_repos/$SOURCE_DIR -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" -o $OUTDIR  --overwrite

