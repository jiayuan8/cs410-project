"""
Referenced from https://github.com/meta-toolkit/metapy-demos
"""

import time
import metapy
import os, json
import pytoml as toml
import sys
env = os.environ["APP_ENV"]
config = json.loads(open('config.json').read())[env]

class Searcher:
    """
    Generate config.toml and create inverted index.
    Wraps the MeTA search engine and its rankers.
    """

    def __init__(self, ds_name, path):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        :param ds_name: dataset name
        :param path: path to dataset (data/author), append ds_name to get full path
        """
        self.default_ranker_cls = metapy.index.OkapiBM25
        cfg = self.generate_config(ds_name, path)
        cwd = os.getcwd()
        with open('stopwords.txt','r') as f:
            stop = f.read()
        os.chdir(path + "/")

        with open('stopwords.txt','w') as f:
            f.write(stop)
        with open(cfg, 'r') as f:
                a = f.read()
        print(cfg,path,a)
        sys.stdout.flush()
        
        self.idx = metapy.index.make_inverted_index(cfg)
        os.chdir(cwd)


    def search(self, query, ranker_name, params={}, num_results=5):
        """
        Accept a query and a ranker and run the provided query with the specified
        ranker.
        :param query: string of query
        :param ranker_name: name of the ranker to be used
        :param params: dict of arguments to be passed into ranker (mutable, do not change)
        :param num_results: return top k relevant documents (k = 5 by default)
        :return: dict of response
        """
        start = time.time()
        q = metapy.index.Document()
        q.content(query)
    
        try:
            ranker_cls = getattr(metapy.index, ranker_name)
        except Exception as e:
            print("Couldn't make '{}' ranker, using default.".format(ranker_name))
            ranker_cls = self.default_ranker_cls
        try:
               ranker = ranker_cls(**params)
        except Exception as e:
            print("Couldn't make '{}' parameter, using default.".format(params.keys()))
            print(e)
            ranker = ranker_cls()

        response = {'query': query, 'results': []}

        results = ranker.score(self.idx, q, num_results)

        for result in results:
            response['results'].append({
                    'score': float(result[1]),
                    'doc_id': result[0],
                    'name': self.idx.doc_name(result[0]),
                    'path': self.idx.doc_path(result[0])
            })

        response['elapsed_time'] = time.time() - start
        return response


    @staticmethod
    def generate_config(ds_name, path):
        """
        Construct config.toml for the dataset &
        Assume line.toml is constructed after uploading
        If already exists, return the config file
        """
        cfg = path + "/" + ds_name + "-config.toml"
        if os.path.isfile(cfg):
                return cfg
        obj = dict()
        obj['prefix'] = "."
        obj['dataset'] = ds_name
        obj['corpus'] = "file.toml"
        obj['index'] = ds_name + "-idx"
        obj['stop-words'] = path + "/" +"stopwords.txt"
        obj['analyzers'] = [dict()]
        analyzer = obj['analyzers'][0]
        analyzer['ngram'] = 1
        analyzer['method'] = "ngram-word"
        analyzer['filter'] = "default-unigram-chain"
        with open(cfg, 'w+') as f:
                toml.dump(f, obj)
        return cfg
