from importlib import import_module
import yaml
import logger

log = logger.Logging("Training")


class Tuning:
    def __init__(self):
        self.config = Tuning.read_config('models.yaml')
        self.model_details = self.config['model_selection']
        self.grid_details = self.config['grid_search']

    @staticmethod
    def read_config(path):
        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            log.log("Error while reading config method")
            print(str(e))

    def setattr_grid(self, params, grid_instance):
        try:
            for key, value in params.items():
                setattr(grid_instance, key, value)
            return grid_instance
        except Exception as e:
            log.log("Error while setting attr method")
            print(str(e))

    def module(self, package_name, algorithm_name):
        try:
            module = import_module(package_name)
            attr = getattr(module, algorithm_name)
            return attr
        except Exception as e:
            log.log("Error while getting module method")
            print(str(e))

    def initialize_model(self):
        try:
            response = []
            log.log("Starting initialize model method")
            for model in self.model_details:
                model_info = dict()
                pkg_name = self.model_details[model]['class']
                module_name = self.model_details[model]['module']
                parameters = self.model_details[model]['params']
                model_obj = self.module(pkg_name, module_name)
                model_obj = model_obj()

                model_info['estimator'] = model_obj
                model_info['module_name'] = module_name
                model_info['package_name'] = pkg_name
                model_info['parameters'] = dict(parameters)

                response.append(model_info)
            log.log("Finished initializing model")
            return response
        except Exception as e:
            print(str(e))

    def grid_execution(self, estimator, params, input_feature, output_feature):
        try:
            log.log("Initializing grid object")
            grid_pkg_name = self.grid_details['module']
            grid_module_name = self.grid_details['class']
            grid_ref = self.module(grid_pkg_name, grid_module_name)
            grid_search = grid_ref(estimator, params)
            grid_search = self.setattr_grid(self.grid_details['params'], grid_search)
            log.log("Fitting data to Grid")
            grid_search.fit(input_feature, output_feature)
            response = {"best_model": grid_search.best_estimator_,
                        "best_parameters": grid_search.best_params_,
                        "best_score": grid_search.best_score_
                        }
            return response

        except Exception as e:
            print(str(e))

    def find_best_model(self, x_train, y_train, model_details):
        try:
            log.log("Finding best model")
            response = []
            for model in model_details:
                result = self.grid_execution(estimator=model['estimator'], params=model['parameters'], input_feature=x_train, output_feature=y_train)
                response.append(result)
            return response

        except Exception as e:
            print(str(e))