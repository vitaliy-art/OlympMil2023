from config.config import Config
from executor import Executor


cfg = Config()
cfg.parse_args()
cfg.validate()

exc = Executor(cfg)
exc.execute()
