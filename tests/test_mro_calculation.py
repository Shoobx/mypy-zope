import os.path
from typing import Optional, List

import pytest
from mypy import options, build
from mypy.build import State
from mypy.modulefinder import BuildSource
from mypy.nodes import SymbolTableNode, TypeInfo

HERE = os.path.abspath(os.path.dirname(__file__))
SAMPLES_DIR = os.path.join(HERE, "samples")


@pytest.fixture(scope="session")
def mypy_cache_dir(tmp_path_factory):
    tdir = tmp_path_factory.mktemp('.mypy_cahe')
    print("Setup cache", str(tdir))
    return str(tdir)


def test_mro_computation_in_forward_reference_to_implementer(mypy_cache_dir: str) -> None:
    sample_name = "forward_reference_to_implementer"

    opts = options.Options()
    opts.show_traceback = True
    opts.namespace_packages = True
    opts.cache_dir = mypy_cache_dir
    opts.plugins = ['mypy_zope:plugin']
    # Config file is needed to load plugins, it doesn't not exist and is not
    # supposed to.
    opts.config_file = 'not_existing_config.ini'

    samplefile = os.path.join(SAMPLES_DIR, f"{sample_name}.py")
    base_dir = os.path.dirname(samplefile)
    with open(samplefile) as f:
        source = BuildSource(
            None,
            module=sample_name,
            text=f.read(),
            base_dir=base_dir,
        )
    result = build.build(sources=[source], options=opts)
    assert result.errors == []

    # Result.graph is a map from module name to state objects.
    state: State = result.graph[sample_name]

    # Find Mypy's representation of the Protocol class.
    node: Optional[SymbolTableNode] = None
    for fullname, symbol_table_node, _type_info in state.tree.local_definitions():
        # Use startswith(...) rather than a direct comparison
        # because the typename includes a line number at the end
        if fullname.startswith(f"{sample_name}.Protocol"):
            node = symbol_table_node
            break

    assert node is not None, f"Failed to find `Protocol` class in mypy's state for {samplefile}"

    mro: List[TypeInfo] = node.node.mro
    # Expected: [
    #   <TypeInfo forward_reference_to_implementer.Protocol@21>,
    #   <TypeInfo builtins.object>,
    #   <TypeInfo forward_reference_to_implementer.IProtocol>,
    # ]
    assert len(mro) == 3
    assert mro[0].fullname.startswith(f"{sample_name}.Protocol")
    assert mro[1].fullname == "builtins.object"
    assert mro[2].fullname == f"{sample_name}.IProtocol"
