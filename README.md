## PrairieLearn Course Repository

## Run command

```bash
docker run -it --rm -p 3000:3000 -v "$PWD:/course" -v "$PWD/pl_ag_jobs:/jobs" -e HOST_JOBS_DIR="$PWD/pl_ag_jobs" -v /var/run/docker.sock:/var/run/docker.sock --add-host=host.docker.internal:172.17.0.1 prairielearn/prairielearn
```

Where `$PWD` is the path to the course directory. For some reason you need to add :/course to the end of the path even though there is no /course folder in the directory. (I spent 1 hour trying to figure this out D:)

If you get an error about **empty section between colors** its likely that PLHOME is not set correctly.

```bash
docker: Error response from daemon: invalid volume specification: '/:course': invalid mount config for type "bind": invalid mount path: 'course' mount path must be absolute.
See 'docker run --help'.
```

### Welcome to PrairieLearn!

The content for your course is stored within this repository.
You can see and edit a live version at [https://prairielearn.com](https://prairielearn.com)

### Getting Started

Learn how to create your first questions and assessments using our [Get Started](https://prairielearn.readthedocs.io/en/latest/getStarted/) tutorial.

### Getting Help

Need help understanding an error or creating content? Check out one of the following resources:

1. Real-time help assistance on PrairieLearn's [Slack `#pl-help` channel](https://prairielearn.com/slack).
1. Looking up the question on our Frequently Asked Question (FAQ) pages: [readthedocs](https://prairielearn.readthedocs.io/en/latest/faq/) and [github-discussions](https://github.com/PrairieLearn/PrairieLearn/discussions/categories/q-a)
1. Attend virtual office hours, which are announced at the start of the
   semester on PrairieLearn's [Slack](https://prairielearn.com/slack)
