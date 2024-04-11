import os

import InstanceManager


class Decoder:
    def __init__(self):
        self.instances = []

    def decode(self, small_only=False, mid_only=False, save=False):
        for type in []:
            for filename in os.scandir("DragonAge_encoded_instances/" + type):
                if filename.is_file():
                    decoded_instance = InstanceManager.to_inst(filename)
                    if len(decoded_instance.map) > 30 and small_only:
                        continue
                    if len(decoded_instance.map) < 30 or len(decoded_instance.map) > 100 and mid_only:
                        continue
                    self.instances.append(decoded_instance)
        for type in ['FL']:
            for filename in os.scandir("Generated_encoded_instances/" + type):
                if filename.is_file():
                    decoded_instance = InstanceManager.to_inst(filename)
                    if len(decoded_instance.map) > 30 and small_only:
                        continue
                    if len(decoded_instance.map) < 30 or len(decoded_instance.map) > 100 and mid_only:
                        continue
                    self.instances.append(decoded_instance)

        if save:
            for instance in self.instances:
                InstanceManager.filter_unconnected(instance)
                InstanceManager.map_reduce(instance)
            for instance in self.instances:
                InstanceManager.to_string(instance, "Reduced_maps")

    def decode_reduced(self,
                       size_lower_bound=None,
                       size_higher_bound=None,
                       horizon_higher_bound=None,
                       types_allowed=('FR', 'MT', 'SC', 'AG001', 'AG05', 'AG01',),
                       specifics=(),
                       max_num=None,
                       sort_by_size=False,
                       file_path=None
                        ):
        for filename in os.scandir(file_path):
            if filename.is_file():
                try:
                    decoded_instance = InstanceManager.to_inst(filename)
                except:
                    print(f"decodeing {filename} failed")
                    continue
                if size_lower_bound is not None and len(decoded_instance.map) < size_lower_bound:
                    continue
                if size_higher_bound is not None and len(decoded_instance.map) > size_higher_bound:
                    continue
                if decoded_instance.type not in types_allowed:
                    continue
                if horizon_higher_bound is not None and horizon_higher_bound > decoded_instance.horizon:
                    continue
                if len(specifics) > 0 and decoded_instance.name not in specifics:
                    continue
                if max_num is not None and len(self.instances) > max_num:
                    break
                self.instances.append(decoded_instance)

        if sort_by_size:
            self.instances = sorted(self.instances, key=lambda inst: len(inst.map))

        return self.instances


