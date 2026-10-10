def test_package_imports():
    import secrethandle
    from secrethandle import cli, experiments, metrics, plotting

    assert secrethandle.__version__ == "0.1.0"
    assert callable(cli.main)
    assert callable(experiments.run_synthetic_demo)
    assert callable(metrics.aggregate_trial_metrics)
    assert callable(plotting.make_plots)
