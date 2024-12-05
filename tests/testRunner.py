import unittest

import testCli
import testWordle
import testSolver
import testVocab
import testEvaluate




loader = unittest.TestLoader()
suite = unittest.TestSuite()


suite.addTests(loader.loadTestsFromModule(testCli))
suite.addTests(loader.loadTestsFromModule(testWordle))
suite.addTests(loader.loadTestsFromModule(testSolver))
suite.addTests(loader.loadTestsFromModule(testVocab))
suite.addTests(loader.loadTestsFromModule(testEvaluate))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)