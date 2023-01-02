from config.config import Config

cfg = Config()
cfg.parse_args()
print(cfg.input_file)
print(cfg.db)
