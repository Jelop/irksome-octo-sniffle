#include <opencv2/opencv.hpp>
#include <iostream>
#include <limits>
#include <random>
#include <chrono>

int k;
int distance_method;
cv::Mat image;
std::vector<cv::Vec3b> clusters;
cv::Mat labels;

double computeEuclidean(cv::Vec3b element, cv::Vec3b centre){
    return sqrt(pow(element[0]-centre[0],2) +
                pow(element[1]-centre[1],2) +
                pow(element[2]-centre[2],2));
}

void initClusters(int type){

    unsigned seed1 = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed1);
    std::uniform_int_distribution<int> randRow(0,image.rows-1);
    std::uniform_int_distribution<int> randCol(0,image.cols-1);
    std::uniform_int_distribution<int> randCluster(0,k-1);

    
    switch(type){

    case 1:
        for(int i = 0; i < k; i++){
            int row = randRow(generator);
            int col = randCol(generator);
            clusters.push_back(image.at<cv::Vec3b>(row,col));
            std::cout << "row: " << row << " col: " << col << std::endl;
            std::cout << image.at<cv::Vec3b>(row,col) << std::endl;
            cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
        }
        break;

    case 2:
        for(int row = 0; row < image.rows; row++){
            for(int col = 0; col < image.cols; col++){
                labels.at<uchar>(row,col) = randCluster(generator);
            }
        }
        for(int cluster = 0; cluster < k; cluster++){
            cv::Vec3i sum = cv::Vec3i(0,0,0);
            int count = 0;
            for(int row = 0; row < labels.rows; row++){
                for(int col = 0; col < labels.cols; col++){
                    if(labels.at<uchar>(row,col) == cluster){
                        cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                        sum[0] += pixel[0];
                        sum[1] += pixel[1];
                        sum[2] += pixel[2];
                        count++;
                    }
                }
            }
            clusters.push_back(cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count));
        }
        break;

    case 3:
        //K-means++ step 1
        clusters.push_back(image.at<cv::Vec3b>(randRow(generator),randCol(generator)));
        //Repeat until k centres have been chosen
        for(int i = 1; i < k; i++){
            cv::Mat distances = cv::Mat(image.rows, image.cols, CV_64FC1);
            for(int row = 0; row < image.rows; row++){
                for(int col = 0; col < image.cols; col++){
                
                    double min_dist = std::numeric_limits<double>::max();
                    for(int centre = 0; centre < clusters.size(); centre++){
                        if(distance_method == 1){
                            double distance = computeEuclidean(image.at<cv::Vec3b>(row,col),
                                                               clusters[centre]);
                            // std::cout << "distance: " << distance << std::endl;
                            if(distance < min_dist)
                                min_dist = distance;
                        }
                    
                    }
                    distances.at<double>(row,col) = pow(min_dist,2);
                }
            }
            
            double weight_sum;
            for(int row = 0; row < distances.rows; row++){
                for(int col = 0; col < distances.cols; col++){
                    weight_sum += distances.at<double>(row,col);
                }
            }
            std::uniform_real_distribution<double> probRange(0, weight_sum);
            double threshold = probRange(generator);
            std::cout << "weight sum: " << weight_sum << std::endl;
            std::cout << "threshold: " << threshold << std::endl;
            bool breakloop = false;
            for(int row = 0; row < distances.rows; row++){
                for(int col = 0; col < distances.cols; col++){
                    double dist_val = distances.at<double>(row,col);
                    if(threshold < dist_val){
                        std::cout << "thresh "<< threshold << " dist_val " << dist_val << std::endl;
                        std::cout << "pushed cluster " << i << std::endl;
                        clusters.push_back(image.at<cv::Vec3b>(row,col));
                        breakloop = true;
                        break;
                    }
                    threshold -= dist_val;
                }
                if(breakloop) break;
            }
                        
                                           
        }
        break;
    }
    
}

void kMeans(){

    for(int i = 0; i < 20; i++){
        std::cout << i << std::endl;
        for(int row = 0; row < image.rows; row++){
            for(int col = 0; col < image.cols; col++){
                //int label = -1;
                double min_dist = std::numeric_limits<double>::max();
                for(int centre = 0; centre < clusters.size(); centre++){
                    cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                    cv::Vec3b cluster = clusters[centre];
                    double distance = computeEuclidean(pixel, cluster);
                    //std::cout << "distance: " << distance << std::endl;
                    if(distance < min_dist){
                        labels.at<uchar>(row,col) = centre;
                        min_dist = distance;
                    }
                }
            }
        }

        for(int centre = 0; centre < clusters.size(); centre++){
            cv::Vec3i sum = cv::Vec3i(0,0,0);
            int count = 0;
            for(int row = 0; row < labels.rows; row++){
                for(int col = 0; col < labels.cols; col++){
                    if(labels.at<uchar>(row,col) == centre){
                        cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                        sum[0] += pixel[0];
                        sum[1] += pixel[1];
                        sum[2] += pixel[2];
                        count++;
                    }
                }
            }
            //random cluster can result in clusters that have no assigned elements
            //Likely still a bug here actually.
            std::cout << sum << std::endl;
            if(count > 0){
                //std::cout << sum << std::endl;
                std::cout << "cluster " << centre << "  before: "\
                          << clusters[centre] << std::endl;
                clusters[centre] = cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count);
                std::cout << "cluster " << centre << "  after: " << clusters[centre]\
                          << std::endl;
            }
        }

    

        for(int centre = 0; centre < clusters.size(); centre++){
            for(int row = 0; row < labels.rows; row++){
                for(int col = 0; col < labels.cols; col++){
                    if(labels.at<uchar>(row,col) == centre){
                        image.at<cv::Vec3b>(row,col) = clusters[centre];
                    }
                }
            }
        }
    }
}
                
int main(int argc, char **argv){


    if(argc != 4){
        std::cout << "Usage: ./kMeans k cluster_init imageFilePath" << std::endl;
        return -1;
    }
    
    k = atoi(argv[1]);
    distance_method = 1;
    image = cv::imread(argv[3]);
    labels = cv::Mat(image.rows, image.cols, CV_8UC1);
    if(!image.data){
        std::cout << "Failed to locate image" << std::endl;
        return -1;
    }
    std::cout << image.type() << std::endl;
    initClusters(atoi(argv[2]));

    kMeans();
    /*int count = 0;
      cv::Vec3b clust = clusters[0];
      for(int i = 0; i < labels.rows; i++){
      for(int j = 0; j < labels.cols; j++){
      cv::Vec3b pixel = image.at<cv::Vec3b>(i,j);
      if(pixel[0] != clust[0] || pixel[1] != clust[1] || pixel[2] != clust[2])
      std::cout << "colour descrepency!!!" << std::endl;
      }
      }*/
    /*for(int i = 0; i < labels.rows; i++){
      for(int j  = 0; j < labels.cols; j++){
      std::cout << (int)labels.at<uchar>(i,j) << " ";
      if(j % 200 == 0) std::cout << std::endl;
      }
      std::cout << "\n" << std::endl;
      }*/
                
    cv::imshow("",image);
    cv::waitKey(0);
    return 0;
}
