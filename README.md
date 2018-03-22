# A-Simple-Crawler
A simple crawler written by python to crwal the images of https://www.pexels.com/

## main point of the idea
* use multiprocessing to accelerate（total of 12).
* to get more urls in one page,every process using deep first traversal to traverse their own url tree.
* using Bloom Filter to avoid url duplication.
