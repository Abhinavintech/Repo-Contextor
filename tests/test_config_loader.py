from rcpack import config_loader


def test_filter_known_keeps_only_known_keys():
    data = {"a": 1, "b": 2, "c": 3}
    known = ["a", "c"]
    out = config_loader._filter_known(data, known)
    assert out == {"a": 1, "c": 3}


def test_merge_precedence_and_defaults():
    defaults = {"x": 1, "y": 2}
    filecfg = {"x": 10, "z": 9}
    clicfg = {"y": 20}
    known = ["x", "y", "z"]

    out = config_loader._merge(defaults, filecfg, clicfg, known)

    # filecfg should override defaults for 'x'
    assert out["x"] == 10
    # cli should override for 'y'
    assert out["y"] == 20
    # unknown in defaults becomes None then filecfg gives value for 'z'
    assert out["z"] == 9
