import os
import inspect

from app.errors import TariffNotDefinedError
from app.tariff_types.tariff_type import TariffType
from app.parking_lot_logger import logger


class TariffFactory:

    def __init__(self, name, price_calc=None):
        self.name = name.lower()
        self._tariff_package = 'app.tariff_types'
        self._tariff_dir = os.path.join('app', 'tariff_types')
        self.price_calc = price_calc

    def get_tariff(self):
        logger.debug(f"Getting tariff {self.name} from factory")
        tariff_modules = self._load_modules()
        try:
            klass = self._get_class_by_name_attr(tariff_modules)
        except TariffNotDefinedError:
            raise
        return klass(self.price_calc)

    def _load_modules(self):
        result = {}
        module_list = os.listdir(self._tariff_dir)
        for module_file in module_list:
            full_path = os.path.abspath(self._tariff_dir) + os.sep + module_file
            if not self._is_dir_or_init(full_path):
                module_name = os.path.splitext(module_file)[0]
                result[module_name] = __import__(f'{self._tariff_package}.{module_name}', fromlist=['*'])
        return result

    def _get_class_by_name_attr(self, modules):
        for module in modules:
            for name, obj in inspect.getmembers(modules[module]):
                if inspect.isclass(obj) and issubclass(obj, TariffType):
                    if obj.name == self.name:
                        return obj
        raise TariffNotDefinedError(self.name)

    @staticmethod
    def _is_dir_or_init(file_or_folder_path):
        if os.path.isdir(file_or_folder_path) or os.path.basename(file_or_folder_path) == "__init__.py":
            return True
        return False
