print("Bundle Upload")
import shotgun_api3 as sg
import tempfile
import atexit
import subprocess
import shutil
import zipfile
import os
import stat

# script_key = os.getenv('BUNDLE_UPLOADER_KEY')
current_branch = os.getenv('GITHUB_REPOSITORY').split('/')[-1]
last_commit_tag = os.getenv('LAST_COMMIT_TAG')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SCRIPT_KEY = os.getenv('SG_SCRIPT_KEY')

sg = sg.Shotgun("https://sg-422south.shotgunstudio.com/", "github-actions", SCRIPT_KEY)


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


class Repository(object):
    """
    Handles operations on a repository.
    """

    @classmethod
    def clone(cls, remote, branch=None, bundle=None):
        """
        Clone a repository from a remote.
        """
        root = tempfile.mkdtemp()
        atexit.register(lambda x: shutil.rmtree(x, onerror=on_rm_error), root)
        bundle_root = os.path.join(root, bundle) if bundle else root
        _branch = "--branch %s" % branch if branch else ""
        cmd = 'git clone -c advice.detachedHead=false --no-hardlinks -q %s %s %s --depth 1' % (
            remote, _branch, bundle_root)
        subprocess.check_call(cmd, shell=True)
        return Repository(root, bundle_root)

    def __init__(self, root, bundle_root=None):
        """
        :param str root: Root of the repository.
        """
        self._root = root
        self._bundle_root = bundle_root

    @property
    def root(self):
        """
        Root of the repository.
        """
        return self._root

    @property
    def bundle_root(self):
        return self._bundle_root

    def add(self, location):
        """
        Add a location to the index.

        :param str location: Location on disk.
        """
        self._git("add", location)

    def commit(self, msg):
        """
        Commit the index.

        :param str msg: Message for the commit.
        """
        self._git("commit", "-m", "{0}".format(msg))

    def push(self):
        """
        Push the repository back to the remote.
        """
        self._git("push", "origin", "master")

    def diff(self):
        """
        Diff with the head.
        """
        self._git("diff", "HEAD")

    @property
    def list_config(self):
        return self._git("config", "--list", with_output=True)

    @property
    def config(self, *args):
        return self._git("config", args, with_output=True)

    @property
    def last_tag(self):
        return self._git("describe", "--tags", "--abbrev=0", with_output=True).strip().decode()

    @property
    def commit_message(self):
        return self._git("log", "-1", "--pretty=format:%B", with_output=True).strip().decode()

    def _git(self, *args, with_output=None):
        """
        Run a git command.

        :param args: List of arguments for the git command.

        If invoking the method as _git("push", "origin", "master"), then the
        result would be subprocess.check_call(["git", "push", "origin", "master"])
        """
        # Disable the pager, we don't want this call to be blocking.
        environ = os.environ.copy()
        environ["PAGER"] = ""
        if with_output:
            return subprocess.check_output(["git"] + list(args), cwd=self._bundle_root, env=environ)
        else:
            return subprocess.check_call(["git"] + list(args), cwd=self._bundle_root, env=environ)


def upload_bundle(bundle, version, site='422South', token=GITHUB_TOKEN):
    # bundle = 'tk-422-utils'
    repo = Repository.clone("https://%s@github.com/%s/%s" % (token, site, bundle), branch=version, bundle=bundle)
    descriptor = "sgtk:descriptor:git?path=https://github.com/%s/%s.git&version=%s" % (site, bundle, version)
    # print("Repo root: ", repo.root)
    # print("Bundle root: ", repo.bundle_root)
    # repo.config("--list")
    # print("Descriptor: ", descriptor)
    # print(os.listdir(repo.root))
    comment = repo.commit_message
    tag = repo.last_tag
    if tag != version:
        raise Exception("Version downloaded %s does not match requested %s " % (tag, version))
    zip_root = tempfile.mkdtemp()
    # print("ziproot %s" % zip_root)
    atexit.register(lambda x: shutil.rmtree(x, onerror=on_rm_error), zip_root)
    zip_filename = "%s/%s-%s.zip" % (zip_root, bundle, version)
    # print("Zip Filename: %s" % zip_filename)
    shutil.rmtree(os.path.join(repo.bundle_root, ".git"), onerror=on_rm_error)
    shutil.rmtree(os.path.join(repo.bundle_root, ".github"), onerror=on_rm_error)
    zip_directory(repo.root, zip_filename)
    # print(os.listdir(repo.root))

    print("%s: %s - %s" % (tag, comment, os.path.basename(zip_filename)))
    if not check_for_bundle(descriptor) and os.path.exists(zip_filename):
        # can create if not a duplicate
        data = {"sg_descriptor": descriptor,
                "description": "%s: %s" % (tag, comment),
                "code": bundle,
                "sg_version": version.replace('v', '')}
        print("Creating SG Bundle entry %s" % data)
        entity = sg.create("CustomNonProjectEntity01", data)
        if not entity:
            raise Exception("Failed to create bundle entry for %s" % bundle)
        sg.upload("CustomNonProjectEntity01", entity['id'], zip_filename, "sg_bundle")
    else:
        raise FileExistsError("Bundle already exists for %s - Uploading skipped" % bundle)


def check_for_bundle(dd):
    entity = sg.find_one(
        "CustomNonProjectEntity01",
        [["sg_descriptor", "is", dd]],
        ["sg_bundle"],
    )
    return entity


def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory_path))


upload_bundle(current_branch, last_commit_tag)
