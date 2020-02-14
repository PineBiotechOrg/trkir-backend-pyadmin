from analysis.constants.enums import \
    FeatureNames, \
    SeasonalDecompositionComponents

FEATURES_FIELDS = FeatureNames.get_values_list()
FEATURES_FIELDS_WITHOUT_DATE = [
    feature for feature in FEATURES_FIELDS
    if feature != FeatureNames.Date.value
]
HEATMAP_FIELDS = ['x', 'y'] + FEATURES_FIELDS_WITHOUT_DATE

BOXPLOT_FIELDS = FEATURES_FIELDS
TIME_WARPING_FIELDS = FEATURES_FIELDS
SEASONAL_DECOMPOSITION_FIELDS = FEATURES_FIELDS + ['component']
SEASONAL_DECOMPOSITION_COMPONENTS = SeasonalDecompositionComponents.get_values_list()
PCA_FIELDS = ['PC1', 'PC2', 'PC3', 'label', 'color']

CAGE_SIZE = [160, 120]
