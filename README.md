<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]

</div>


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">mc-auto-voter</h3>

  <p align="center">
    A simple automation script in python to perform automatic server voting for cracked minecraft servers. 
    <br />
    <a href="https://github.com/neelnix/autoVoter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/neelnix/autoVoer">View Demo</a>
    &middot;
    <a href="https://github.com/neelnix/autoVoter/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/neelnix/autoVoter/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-for-the-script">Installation for the script</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The script is fully customizable and rapidly changeable. All the automation tasks for each specific site are divided into its own class, thus enabling rapid adaptability to any change in website layout.
All the automation tasks are handled for worst case scenarios, all of it then saved in a log and showed to the user during runtime and automatic retrial of failed votes.

<strong> For now the scripts supports automatic voting for the servers, pika-network and jartex-network. </strong>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* To run using the released binary, nothing is required, the script automatically downloads the required chromium web-drivers and other dependencies.
* To run the script itself, python in a virtual environment is preferred.

### Installation for the script

1. Clone the repo
   ```sh
   git clone https://github.com/neelnix/autoVoter.git
   ```
3. Install the python packages required
   ```sh
   pip install -r requirements.txt
   ```
5. Either you can have the script automatically download the required chromium binaries or manually download the chromium binaries
   ```sh
   playwright install chromium
   patchright install chromium
   ```
   Any one these two commands will work, only chromium is needed as patchright supports only chromium.
   If using the automatic download, then the downloaded binaries will be places at `project_dir/browsers`

<!-- USAGE EXAMPLES -->
## Usage

1. Both the scipt and the released binary needs a .env file placed in the root of the `project_dir` to work.
   The required fields and values are attached below for the .env file, change this values accordingly.

```
    #username to use for voting
    MC_USERNAME = "steve"
    
    #retry count, can be set to 0
    RETRY_COUNT = 2
    
    #whether to inform the user if there is a updated version of the app
    CHECK_FOR_UPDATE = true
    
    #Whether to run the automation in headless mode or not
    RUN_HEADLESS = true
    
    #Urls to try to vote for jartex, urls can be changed here to accomodate for any change in the urls provided on the jartex network vote page
    URLS_JARTEX = "https://topminecraftservers.org/vote/18687,https://best-minecraft-servers.co/server-jartexnetwork.4402/vote,https://www.minerank.com/jartexnetwork/vote,https://minecraft.buzz/vote/jartexnetwork,https://minecraftkrant.nl/server/jartexnetwork/vote,https://minecraft-mp.com/server/52462/vote/,https://minecraft-server-list.com/server/288369/vote/"
    
    #Urls to try to vote for pika, urls can be changed here to accomodate for any change in the urls provided on the pika network vote page
    URLS_PIKA = "https://topminecraftservers.org/vote/21765,https://best-minecraft-servers.co/server-pikanetwork-bestq-pika-host.4401/vote,https://www.minerank.com/pikanetwork/vote,https://minecraft.buzz/vote/pikanetwork,https://minecraftkrant.nl/server/pikanetwork/vote,https://minecraft-mp.com/server/41366/vote/,https://minecraft-server-list.com/server/424827/vote/"
    
    #Domains to block to stop inteeference from popups, required for one site at the time
    DOMAINS_TO_BLOCK = "opulentsylvan.com,copycarpenter.com"
 ```
2. To Vote for pika-network
   ```sh
   autoVoter.exe pika
   ```
   ```sh
   python src/main.py pika 
   ```
3. To vote for jartex
   ```sh
   autoVoter.exe jartex
   ```
   ```sh
   python src/main.py jartex
   ```
4.  Optionally you can use, `autoVoter.exe pika -u Alex -rc 5`
   
    `-u` will set the username for that specific run to the given value and `-rc` will set the retry count to the given value. This args overwrite the .env values.
   

<!-- CONTRIBUTING -->
## Contributing

Any contributions are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!


### Top contributors:

<a href="https://github.com/neelnix/autoVoter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=neelnix/autoVoter" alt="contrib.rocks image" />
</a>


<!-- LICENSE -->
## License

Distributed under the MIT license. See `LICENSE.txt` for more information.


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Scrapling](https://github.com/d4vinci/Scrapling)
* [Readme Template](https://github.com/othneildrew/Best-README-Template)
* [pathright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/neelnix/mc-auto-voter.svg?style=for-the-badge
[contributors-url]: https://github.com/neelnix/mc-auto-voter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/neelnix/mc-auto-voter.svg?style=for-the-badge
[forks-url]: https://github.com/neelnix/mc-auto-voter/network/members
[stars-shield]: https://img.shields.io/github/stars/neelnix/mc-auto-voter.svg?style=for-the-badge
[stars-url]: https://github.com/neelnix/mc-auto-voter/stargazers
[issues-shield]: https://img.shields.io/github/issues/neelnix/mc-auto-voter.svg?style=for-the-badge
[issues-url]: https://github.com/neelnix/mc-auto-voter/issues
[license-shield]: https://img.shields.io/github/license/neelnix/mc-auto-voter.svg?style=for-the-badge
[license-url]: https://github.com/neelnix/mc-auto-voter/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
