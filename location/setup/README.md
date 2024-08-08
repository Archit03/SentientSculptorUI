[Location Projects for OpenWebUI](../)
# Open WebUI Setup
<!--Pinecone -->

If you already have an "open-webui" Docker container, your OpenWebUI server may already be running at [localhost:3000](http://localhost:3000) (since Docker restarts it when you start your computer).  You can now [train with a web page](train).

Use our [Docker Setup](docker) for a quick install with Ollama for loading models. The page also includes experiments in which we extract backend files to edit in a Webroot. We're not sure if un-built frontend files can reside in OpenWebUI Docker container images.
<br>


# Install for Building Locally (without Docker)

### Use our conda-start.sh script to install with one step

These steps are for programmers planning to edit and build locally. Visit [localhost:8080](http://localhost:8080) if you've already install.  
After the initial one hour or more install, it only take a minute to restart the server using the same conda-start.sh command below.

If you machine needs updates, our [node, python and conda upgrade page](https://model.earth/io/coders/python) is helpful.  
If you're not planning to edit, you can install faster using a [local Docker instance](docker).  

We recommend using GitHub Desktop to pull [our projects repo](https://github.com/modelearth/projects/) to your computer, or you can clone with a command:

	git clone https://github.com/modelearth/projects.git
	cd projects/

Check that you have cmd apps available, include a 3.11 version of python.

	conda --version
	python3.11 --version
	node --version
	npm --version

On Windows: You can run the "start.bat" steps on [Open WebUI Getting Started](https://docs.openwebui.com/getting-started/). We've documented how to deploy the [Windows steps with conda](https://github.com/ModelEarth/projects/blob/gcp/location/setup/guides/local.md)

On Mac and Linux: Run the following in the root of the "projects" folder. Our [conda-start.sh](https://github.com/ModelEarth/projects/blob/main/location/setup/script/conda-start.sh) script invokes python3.11 so you might need [pyenv](https://model.earth/io/coders/python).
	
	bash location/setup/script/conda-start.sh

That's it. Wait an hour or two to finish, then view the site here:

[http://localhost:8080](http://localhost:8080)

Now you can build to apply changes from "src" and "backup".

	npm run build

"npm run build" seems to break secure https 0.0.0.0:8080 hosting.  
(Perhaps because the test included the external localsite.js file.)

Don't use `npm run dev` it only hosts the frontend and you'll get a message that backend did not build. 


### Related Notes

As of July 2024, OpenWebUI has issues with python 3.12, so we use python 3.11 in conda-start.sh.  Here are our notes of checking [your local python version and install nvm](../../../io/coders/python/) to host multiple version of python.

Check that you have npm installed. If not, [install node project manager](../../../io/coders/python/)

	npm -v

View a list of your conda environments.
If none are found, [download from Anaconda.com](https://www.anaconda.com/download)

	conda env list  


The conda-start.sh script uses commands from [Open WebUI Getting Started](https://docs.openwebui.com/getting-started/) for building locally.  

The commands incude the following:

	# Building Frontend Using Node
	npm i
	npm run build

	# Serving Frontend with the Backend
	cd ./backend
	pip install -r requirements.txt -U

	bash start.sh

We created conda-start.sh because `bash start.sh` above fails when Llama is not available - since it uses the settings config file.

Our conda-start.sh runs the backend in a virtual environment.  
You could optionally run the following first too. We haven't confirmed the install works when running this first.

	python3.11 -m venv env
	source env/bin/activate

### RAM error

A RAM error shut down the local site: [1 leaked semaphore](https://github.com/lllyasviel/Fooocus/discussions/2690)  
The CPU was not running when this occurred.

<!--
The following restarted the frontend at [localhost:5173](http://localhost:5173/)
After a couple minutes you'll see "Open WebUI Backend Required"

	npm run dev
-->
<!--
Running the pre-existing bash start.sh results in:

Loading WEBUI_SECRET_KEY from file, not provided as an environment variable.
Loading WEBUI_SECRET_KEY from .webui_secret_key
start.sh: line 23: ${USE_OLLAMA_DOCKER,,}: bad substitution
start.sh: line 25: ${USE_CUDA_DOCKER,,}: bad substitution
start.sh: line 52: exec: uvicorn: not found

Is there a fast way to reopen the conda instance?
-->

**Restart server**

Restarting the server only takes a couple minutes. Use the same command as above.  
Choose the existing conda environment by saying "no" when asked to reinstall.

	bash location/setup/script/conda-start.sh


## Edit in our Open WebUI "projects/location" folder

The "projects/location" folder is where we'll edit enhancements to the "src" folder.  
We'll merge our enhancments into "src-merged" so we don't have sync issues with open-webui.

We also edit index.html and active.md in our "projects" fork root. We added those files, so they won't have sync conflicts with the parent repo.

TO DO:

Place updates in our custom "projects/location" folder.

Add CUSTOM START and CUSTOM END around our custom code. Create a python script that uses those strings to insert our custom code from projects/location into the "src" version and save the merged files in "src-merged". (ChatGPT could help figure out how to insert the custom text.)

Point our "npm run build" at the "src-merged" folder.
