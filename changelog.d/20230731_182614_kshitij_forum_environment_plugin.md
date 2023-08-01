- [Improvement] Introduces the `FORUM_ENV` filter to which any additional forum
  which simplifies management of environment variables for the forum service. 
  Additional environment variables can be added to this filter, and existing
  values can be removed as needed by plugins. These are rendered into the new 
  `forum-k8s-env` and `forum-local-env` patches for the kubernetes and docker
  configs respectively. (by @xitij2000)