

<!-- PROJECT LOGO -->
<!--<br />-->
<!--<p align="center">-->
<!--  <a href="https://github.com/PandaBoi/fMRI_Domain_Adaptation">-->
<!--    <img src="images/logo.png" alt="Logo" width="80" height="80">-->
<!--  </a>-->

  <h3 align="center">Multi-Site Domain Adaptation for rs-fMRI Classifications</h3>

  <p align="center">
    Applying various multi-site DA models for different types of rs-fMRI based classifications
    <!--<br />-->
    <!--<a href="https://github.com/PandaBoi/fMRI_Domain_Adaptation"><strong>Explore the docs »</strong></a>-->
<!--    <br />-->
<!--    <br />-->
<!--    <a href="https://github.com/PandaBoi/fMRI_Domain_Adaptation">View Demo</a>-->
<!--    ·-->
<!--    <a href="https://github.com/PandaBoi/fMRI_Domain_Adaptation/issues">Report Bug</a>-->
<!--    ·-->
<!--    <a href="https://github.com/PandaBoi/fMRI_Domain_Adaptation/issues">Request Feature</a>-->
<!--  </p>-->
<!--</p>-->



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repo contains the PyTorch implementation of the experiments carried out in (cite). Most of the code used for building models is adapted from the [DARN repo](https://github.com/junfengwen/DARN). 


### Built With

* Scipy 1.5.4
* Pandas 1.1.4
* Imbalanced_learn 0.7.0
* EasyDict 1.9
* Numpy 1.19.4
* PyTorch 1.7.0
* Nilearn 0.7.0
* Nibabel 3.2.1
* Imbalanced_learn 0.0
* Matplotlib 3.3.3


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/PandaBoi/fMRI_Domain_Adaptation.git
   ```
2. Install requirements.txt packages
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage

Once the repo has been downloaded and the libraries are installed, the experiments can be found in `EXP1.ipynb` notebook.
The other files consist of:

* models.py : implementation of multi-site DA models in PyTorch
* utils.py : common utility functions useful during training and testing
* module.py : helper functions such as GRL and Projection functions utilized by the DA models
* load_data.py : functions to load and convert data into format usable for analysis
  * In this work, [ABIDE]() and [ADHD200]() datasets were used which are publicly available.
  * To add your own custom multi-site data, the fMRI data is to be:
    - Converted to functional connectivity matrix and flattened ( discarding diagonal).
    - Stored in a dictionary with keys as the site name.
    - Each site holds another dictonary with keys `data` and `label`.
    - The flattened vectors for the data present in each site is stacked and stored along with their labels in this sub-dictionary.

The data to be used needs to be placed in a `data/` folder and the necessary changes have to be made in the notebook by feeding in the data_path.



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/PandaBoi/fMRI_Domain_Adaptation/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Rohan Panda - rohanpanda.99@gmail.com

Project Link: [https://github.com/PandaBoi/fMRI_Domain_Adaptation](https://github.com/PandaBoi/fMRI_Domain_Adaptation)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Dr. Russ Greiner](https://sites.google.com/view/drrussellgreiner/home?authuser=0)
* [Dr. Sunil Kalmady Vasu](https://github.com/sunilkalmadi)
* [Jungfen Wen](https://github.com/junfengwen)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!--[contributors-shield]: https://img.shields.io/github/contributors/PandaBoi/repo.svg?style=for-the-badge-->
<!--[contributors-url]: https://github.com/PandaBoi/repo/graphs/contributors-->
<!--[forks-shield]: https://img.shields.io/github/forks/PandaBoi/repo.svg?style=for-the-badge-->
<!--[forks-url]: https://github.com/PandaBoi/repo/network/members-->
<!--[stars-shield]: https://img.shields.io/github/stars/PandaBoi/repo.svg?style=for-the-badge-->
<!--[stars-url]: https://github.com/PandaBoi/repo/stargazers-->
<!--[issues-shield]: https://img.shields.io/github/issues/PandaBoi/repo.svg?style=for-the-badge-->
<!--[issues-url]: https://github.com/PandaBoi/repo/issues-->
<!--[license-shield]: https://img.shields.io/github/license/PandaBoi/repo.svg?style=for-the-badge-->
<!--[license-url]: https://github.com/PandaBoi/repo/blob/master/LICENSE.txt-->
<!--[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555-->
<!--[linkedin-url]: https://linkedin.com/in/PandaBoi-->

