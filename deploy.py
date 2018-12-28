import tarfile
import urllib.request
import logging
import os.path
import subprocess
import time

# Logger configurations

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    filename='deploy.log',
                    format='%(asctime)s [%(levelname)s] '
                           '%(funcName)-20s : %(message)s')


def exit_error(msg):
    """print error message and quit the script"""
    logging.error(msg)
    logging.error("Deployment failed")
    raise SystemExit


def download_file(url, file_name):
    """download file from given url if not exists in current directory"""
    if os.path.isfile(file_name):
        logging.info("{fname} already exists, skipping download"
                     .format(fname=file_name))
        return
    logging.info("about to download {fname} from url: {url}"
                 .format(fname=file_name, url=url))
    try:
        urllib.request.urlretrieve(url, file_name)
    except Exception as e:
        exit_error(e)
    logging.info("download completed")


def extract_tar_gz(file_name, extract_path):
    """extract .tar.gz file to a given path"""
    logging.info("extracting {fname} to {path}"
                .format(fname=file_name, path=extract_path))
    try:
        tar = tarfile.open(file_name, "r:gz")
        tar.extractall(path=extract_path)
        tar.close()
    except Exception as e:
        exit_error(e)
    logging.info("all files extracted")


def run_cmd(cmd):
    """run shell command"""
    logging.info(cmd)
    try:
        process = subprocess.Popen(cmd.split(),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        out, _ = process.communicate()
        out = out.decode().split('\n')
        if process.returncode != 0:
            for line in out:
                logging.error(line)
            raise ChildProcessError("command failed")
        for line in out:
            logging.info(line)
    except Exception as e:
        logging.error("failed to run command: {cmd}".format(cmd=cmd))
        exit_error(e)


def docker_handler():
    """run all docker-compose steps, exit the script if fail"""
    docker_commands = ["docker-compose build",
                       "docker-compose down",
                       "docker-compose up -d"]
    for command in docker_commands:
        run_cmd(command)


def health_check(url):
    """check if the application is app and running"""
    wait_loops = 4
    for i in range(wait_loops):
        logging.info("checking application's health")
        try:
            status = urllib.request.urlopen(url).getcode()
            break
        except Exception as e:
            if i == wait_loops-1:
                logging.error("failed to check application's health")
                exit_error(e)
            logging.error("trying again ({now}/{total})"
                          .format(now=i+1, total=wait_loops))
            time.sleep(1)
    if status == 200:
        logging.info("Deployment passed, received 200 OK")
    elif status == 500:
        msg = "received 500, failing deployment..."
        exit_error(msg)


################################################################################
# VARIABLES
################################################################################
bucket_name = "devops-exercise"
tar_file = "pandapics.tar.gz"
download_url = "http://s3.eu-central-1.amazonaws.com/{bucket}/{file}"\
    .format(bucket=bucket_name, file=tar_file)
images_path = "app/public/images"
base_url = "http://0.0.0.0:3000"
health_url = "{base}/health".format(base=base_url)


################################################################################
# MAIN
################################################################################
download_file(download_url, tar_file)
extract_tar_gz(tar_file, images_path)
docker_handler()
health_check(health_url)
