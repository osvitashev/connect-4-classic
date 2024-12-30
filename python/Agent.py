class Agent:
    def __init__(self, searchDepth):
        self._searchDepth = searchDepth
        self._nodeCount = 1
    
    def getNodeCount(self):
        return self._nodeCount