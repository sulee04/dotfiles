import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('setup', Path(__file__).resolve().parents[1] / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


@unittest.skipUnless(shutil.which('stow'), 'GNU Stow required')
class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.home.mkdir()
        self.repo = Path(self.temp.name) / 'checkout'
        shutil.copytree(setup.REPO, self.repo, symlinks=True,
                        ignore=shutil.ignore_patterns('.git', '__pycache__'))
        env = patch.object(Path, 'home', return_value=self.home)
        env.start()
        self.addCleanup(env.stop)
        repo_patch = patch.object(setup, 'REPO', self.repo)
        repo_patch.start()
        self.addCleanup(repo_patch.stop)
        self.instance = setup.Setup(SimpleNamespace())

    def test_fresh_checkout_and_repeat(self):
        self.instance.configs()
        config = self.home / '.config/yazi/yazi.toml'
        helper = self.home / '.local/bin/nvim-yazi-editor'
        self.assertEqual(config.resolve(), self.repo / 'vim/.config/nvim/integrations/yazi/yazi.toml')
        self.assertTrue(os.access(helper, os.X_OK))
        self.assertTrue((self.home / '.config/nvim/README.md').exists())
        self.instance.configs()
        self.assertFalse(self.instance.backups.exists())

    def test_conflicts_are_backed_up(self):
        config = self.home / '.config/zellij/config.kdl'
        config.parent.mkdir(parents=True)
        config.write_text('old config')
        unrelated = config.parent / 'other.kdl'
        unrelated.write_text('keep me')
        self.instance.configs()
        self.assertEqual((self.instance.backups / '.config/zellij/config.kdl').read_text(), 'old config')
        self.assertEqual(unrelated.read_text(), 'keep me')

    def test_absolute_links_are_replaced(self):
        config = self.home / '.config/yazi/yazi.toml'
        config.parent.mkdir(parents=True)
        config.symlink_to(self.repo / 'vim/.config/nvim/integrations/yazi/yazi.toml')
        self.instance.configs()
        self.assertFalse(os.path.isabs(os.readlink(config)))
        self.assertTrue((self.instance.backups / '.config/yazi/yazi.toml').is_symlink())

    def test_failure_restores_original_config(self):
        config = self.home / '.codex/config.toml'
        config.parent.mkdir()
        config.write_text('original')
        with patch.object(setup, 'run', side_effect=subprocess.CalledProcessError(1, 'stow')):
            with self.assertRaises(subprocess.CalledProcessError):
                self.instance.configs()
        self.assertEqual(config.read_text(), 'original')

    def test_external_parent_symlink_is_untouched(self):
        other = Path(self.temp.name) / 'external'
        other.mkdir()
        (self.home / '.config').symlink_to(other)
        with self.assertRaisesRegex(RuntimeError, 'links outside'):
            self.instance.configs()
        self.assertEqual(list(other.iterdir()), [])
        self.assertTrue((self.home / '.config').is_symlink())
