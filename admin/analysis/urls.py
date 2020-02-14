from django.conf.urls import url

from .views.analysis_projects import AnalysisProjectsViews
from .views.preprocessing import PreprocessingViews
from .views.methods import MethodsViews

# analysis projects
analysis_list = AnalysisProjectsViews.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'delete',
})

analysis_from_favorites = AnalysisProjectsViews.as_view({
    'post': 'create_from_favorites',
})

analysis_management = AnalysisProjectsViews.as_view({
    'get': 'retrieve',
    'put': 'add_mice_to_project',
    'post': 'update_info',
})

# preprocessing
mouse_features_management = PreprocessingViews.as_view({
    'get': 'get_mouse_features',
})

mouse_averaged_features_management = PreprocessingViews.as_view({
    'get': 'get_mouse_averaged_features',
    'post': 'make_mouse_averaged_features',
})

mouse_normalized_features_management = PreprocessingViews.as_view({
    'get': 'get_mouse_normalized_features',
    'post': 'make_mouse_normalized_features',
})

mouse_averaged_normalized_features_management = PreprocessingViews.as_view({
    'get': 'get_mouse_averaged_normalized_features',
    'post': 'make_mouse_averaged_normalized_features',
})

mouse_average_healthy_management = PreprocessingViews.as_view({
    'get': 'get_mouse_average_healthy',
    'post': 'make_mouse_average_healthy',
})

mouse_normalized_average_healthy_management = PreprocessingViews.as_view({
    'get': 'get_mouse_normalized_average_healthy',
    'post': 'make_mouse_normalized_average_healthy',
})

# methods
mouse_heatmap_management = MethodsViews.as_view({
    'get': 'get_mouse_heatmap',
    'post': 'make_mouse_heatmap',
})

mouse_boxplot_management = MethodsViews.as_view({
    'get': 'get_mouse_boxplot',
    'post': 'make_mouse_boxplot',
})

mouse_time_warping_management = MethodsViews.as_view({
    'get': 'get_mouse_time_warping',
    'post': 'make_mouse_time_warping',
})

mouse_seasonal_decomposition_management = MethodsViews.as_view({
    'get': 'get_mouse_seasonal_decomposition',
    'post': 'make_mouse_seasonal_decomposition',
})

experiment_pca_management = MethodsViews.as_view({
    'get': 'get_experiment_pca',
    'post': 'make_experiment_pca',
})

analysis_pca_management = MethodsViews.as_view({
    'get': 'get_project_pca',
    'post': 'make_project_pca',
})

urlpatterns = [
    # analysis projects
    url(
        r'^$',
        analysis_list,
        name='analysis-list'
    ),
    url(
        r'^from_favorites/?$',
        analysis_from_favorites,
        name='analysis-from_favorites'
    ),
    url(
        r'^analysis/(?P<pk>[0-9]+)/?$',
        analysis_management,
        name='analysis-management'
    ),

    # preprocessing
    url(
        r'^mouse/(?P<pk>[0-9]+)/features/?$',
        mouse_features_management,
        name='mouse-features-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/averaged_features/?$',
        mouse_averaged_features_management,
        name='mouse-average-features-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/normalized_features/?$',
        mouse_normalized_features_management,
        name='mouse-normalized-features-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/averaged_normalized_features/?$',
        mouse_averaged_normalized_features_management,
        name='mouse-averaged-normalized-features-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/average_healthy/?$',
        mouse_average_healthy_management,
        name='mouse-average-healthy-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/normalized_average_healthy/?$',
        mouse_normalized_average_healthy_management,
        name='mouse-normalized_average-healthy-management'
    ),

    #  methods
    url(
        r'^mouse/(?P<pk>[0-9]+)/heatmap/?$',
        mouse_heatmap_management,
        name='mouse-heatmap-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/boxplot/?$',
        mouse_boxplot_management,
        name='mouse-boxplot-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/time_warping/?$',
        mouse_time_warping_management,
        name='mouse-time-warping-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/seasonal_decomposition/?$',
        mouse_seasonal_decomposition_management,
        name='mouse-seasonal-decomposition-management'
    ),
    url(
        r'^experiment/(?P<pk>[0-9]+)/pca/?$',
        experiment_pca_management,
        name='experiment-pca-management'
    ),
    url(
        r'^analysis/(?P<pk>[0-9]+)/pca/?$',
        analysis_pca_management,
        name='analysis-pca-management'
    ),
]
