# Simply you need to have all the required files in golden-flame folder.

# Use an official Node.js image as the base
FROM node:lts

# Set the working directory in the container
WORKDIR /app

# Copy the available package.json and package-lock.json to the working directory
COPY golden-flame/package.json golden-flame/package-lock.json*  golden-flame/yarn.lock* golden-flame/pnpm-lock.yaml* ./

# Copy the rest of the application source code
COPY golden-flame/. ./

# Install app dependencies
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm i; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
  # Allow install without lockfile, so example works even without Node.js installed locally
  else echo "Warning: Lockfile not found. It is recommended to commit lockfiles to version control." && yarn install; \
  fi


# Start vue.js in development mode based on the preferred package manager
CMD \
if [ -f yarn.lock ]; then yarn dev --host; \
elif [ -f package-lock.json ]; then npm run dev -- --host; \
elif [ -f pnpm-lock.yaml ]; then pnpm dev --host; \
else yarn dev --host; \
fi

#### FIRST TIME Setup when you don't have the config file. Follow these steps:
#### Since I don't have the Vue config files at the beginning, I need to create a Vue app to get the required files.
#### I first create a container using the dockerfile to start a Vue project with the recent available updates from Vue website
#### Then copy the content of the created vue-project folder into the root directory of you local working environment. 
#### Utilize the existing docker compose file to create a new container and work with that from there after. 
#### You can now delete the first container you created. 

# Comment out the last three lines of the Dockerfile (COPY and COPY and RUN)

# Command prompt for first time building image
# docker build -t kitsune-vue-image .

# Command prompt to run
# docker run -it -p 5173:5173 --name GoldenFlame -v .:/app kitsune-vue-image /bin/bash

# For the first time you need to follow the instruction of https://vuejs.org/guide/quick-start.html to build the app

# Copy the whole created folder into the root directory of your local working environment

# modify the vite.config.js file 

# export default defineConfig({
#   plugins: [vue(), vueDevTools()],
#   resolve: {
#     alias: {
#       "@": fileURLToPath(new URL("./src", import.meta.url)),
#     },
#   },
#   server: {
#     host: "0.0.0.0",
#     port: 5173,
#   },
# });


#### Later, to test or access directly to the container without docker compose
# To go inside the container you may use
# docker start my-vue-app
# docker exec -it my-vue-app /bin/bash
# cd vue-project
# npm run dev
