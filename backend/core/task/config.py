

# Task Config
class TaskConfig:
  def __init__(self, config, module_options):
    self._config = config
    # Options
    self.once = self._config.once
    self.signal = self._config.signal
    self.autostart = self._config.autostart

    self.delay = self._config.delay

    # Repeat only once is false
    self.repeat = self._config.repeat if not self.once else None
    self.repeat_count = self._config.repeat_count if not self.once else None

    # Initial Options
    # Original module options manifest
    self._module_options = module_options
    self._options = [self._config.options]
  
  # Not required
  def get(self, key, fallback=None):
    return self._config.get(key, fallback)

  @property
  def options(self) -> dict[str, str]:
    return { name: option["result"] for name, option in self._options[-1].items() }

  # Get Raw Options
  def get_raw_options(self):
    # values dict to update in 2nd dict
    values = { name: option["value"] for name, option in self._options[-1].items() }

    return {
      name: {**opt.model_dump(), "value": values.get(name, opt.value)}
      for name, opt in self._module_options.items()
    }
  
  # Update options with k, v type
  def update_options(self, options):
    self._options.append(options)

