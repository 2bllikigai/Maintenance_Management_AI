# models/__init__.py
from . import asset_category            # Load cái này đầu tiên vì nó độc lập
from . import asset
from . import maintenance
from . import asset_depreciation_line
from . import asset_request             # Load cái này cuối cùng