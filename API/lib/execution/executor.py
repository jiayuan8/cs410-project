import json
import os
import subprocess

class Executor:
    """File is uploaded in Azure as master/executor.py.
    This is the main entrypoint on worker VMs.
    """

    def execute(self):
        print("Beginning execution...")
        self._execute_prescript()
        self._execute_entrypoint()

    def parse(self, config_path):
        config_exists = os.path.exists(config_path)
        if not config_exists:
            raise("ERROR: Missing required configuration file called 'livedatalab_config.json'")

        self.config = json.loads(open(config_path).read())

        if "entrypoint" not in self.config:
            raise("ERROR: Missing required field 'entrypoint' in 'livedatalab_config.json'")

        self.entrypoint = 'python -u /azure/scoring/' + self.config["entrypoint"] + '.py'

        if "prescript_commands" not in self.config:
            self.prescript_commands = []
        else:
            self.prescript_commands = self.config["prescript_commands"]

    def _execute_prescript(self):
        for cmd in self.prescript_commands:
            subprocess.call(cmd.split(" "))

    def _execute_entrypoint(self):
        p = subprocess.Popen(self.entrypoint.split(" "), bufsize=1, universal_newlines=True, stdout=subprocess.PIPE)
        
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() is not None:
                break
            if line:
                print(line.rstrip())

        exit(p.poll())

if __name__ == "__main__":
    executor = Executor()
    executor.parse("livedatalab_config.json")
    executor.execute()
