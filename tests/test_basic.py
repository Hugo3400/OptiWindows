"""
Tests unitaires pour OptiWindows
Vérifie le bon fonctionnement des modules principaux
"""

import unittest
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.system_info import SystemInfo
from utils.logger import get_logger, setup_logger
from utils.config_manager import ConfigManager
from utils.admin_check import is_admin


class TestSystemInfo(unittest.TestCase):
    """Tests pour le module SystemInfo"""
    
    def setUp(self):
        self.sysinfo = SystemInfo()
    
    def test_get_cpu_usage(self):
        """Test récupération utilisation CPU"""
        cpu = self.sysinfo.get_cpu_usage()
        self.assertIsInstance(cpu, (int, float))
        self.assertGreaterEqual(cpu, 0)
        self.assertLessEqual(cpu, 100)
    
    def test_get_memory_info(self):
        """Test récupération info mémoire"""
        mem = self.sysinfo.get_memory_info()
        self.assertIsInstance(mem, dict)
        self.assertIn('total', mem)
        self.assertIn('used', mem)
        self.assertIn('percent', mem)
        self.assertGreaterEqual(mem['percent'], 0)
        self.assertLessEqual(mem['percent'], 100)
    
    def test_get_disk_info(self):
        """Test récupération info disque"""
        disk = self.sysinfo.get_disk_info()
        self.assertIsInstance(disk, dict)
        self.assertIn('total', disk)
        self.assertIn('used', disk)
        self.assertIn('free', disk)
    
    def test_get_windows_version(self):
        """Test récupération version Windows"""
        version = self.sysinfo.get_windows_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


class TestLogger(unittest.TestCase):
    """Tests pour le module Logger"""
    
    def setUp(self):
        self.logger = get_logger("test")
        self.test_log_file = Path("logs/optiwindows.log")
    
    def test_logger_creation(self):
        """Test création du logger"""
        self.assertIsNotNone(self.logger)
    
    def test_log_info(self):
        """Test logging info"""
        self.logger.info("Test info message")
        # Vérifier que le message est bien loggé
        if self.test_log_file.exists():
            content = self.test_log_file.read_text()
            self.assertIn("Test info message", content)
    
    def test_log_error(self):
        """Test logging erreur"""
        self.logger.error("Test error message")
        if self.test_log_file.exists():
            content = self.test_log_file.read_text()
            self.assertIn("Test error message", content)


class TestConfigManager(unittest.TestCase):
    """Tests pour le gestionnaire de configuration"""
    
    def setUp(self):
        self.config = ConfigManager()
    
    def test_load_settings(self):
        """Test chargement des paramètres"""
        settings = self.config.settings
        self.assertIsInstance(settings, dict)
        self.assertIn('version', settings)
    
    def test_get_setting(self):
        """Test récupération d'un paramètre"""
        version = self.config.get_setting('version')
        self.assertIsNotNone(version)
    
    def test_set_setting(self):
        """Test définition d'un paramètre"""
        result = self.config.set_setting('test_key', 'test_value')
        self.assertTrue(result)
        
        value = self.config.get_setting('test_key')
        self.assertEqual(value, 'test_value')
    
    def test_get_profiles(self):
        """Test récupération des profils"""
        profiles = self.config.get_all_profiles()
        self.assertIsInstance(profiles, dict)
        self.assertGreater(len(profiles), 0)


class TestAdminCheck(unittest.TestCase):
    """Tests pour la vérification admin"""
    
    def test_is_admin(self):
        """Test vérification droits admin"""
        result = is_admin()
        self.assertIsInstance(result, bool)
        # Note: Le résultat dépend de comment le test est lancé
        # On vérifie juste que la fonction retourne un bool


def run_tests():
    """Lance tous les tests"""
    # Créer le répertoire de logs si nécessaire
    Path("logs").mkdir(exist_ok=True)
    
    # Créer une suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestSystemInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestAdminCheck))
    
    # Lancer les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retourner le résultat
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
