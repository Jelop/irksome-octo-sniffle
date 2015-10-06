#include <opencv2/opencv.hpp>
#include <iostream>
#include <limits>
#include <random>
#include <chrono>
#include <cstdlib>

double DIST_FACTOR = 0;
int k;
int distance_method;
cv::Mat image;
std::vector<cv::Vec3b> clusters;
std::vector<cv::Point2i> cluster_locations;
cv::Mat labels;

double computeDistance(int row, int col, int cluster_number){

    cv::Vec3b element = image.at<cv::Vec3b>(row,col);
    cv::Vec3b centre = clusters[cluster_number];
    cv::Point2i location = cluster_locations[cluster_number];
    
    switch(distance_method){

    case 1:
        
        return sqrt(pow(element[0]-centre[0],2) +
                    pow(element[1]-centre[1],2) +
                    pow(element[2]-centre[2],2));
        break;

    case 2:

        element[0] = ((float)element[0]/180) * 256;
        centre[0] = ((float)centre[0]/180) * 256;
        return sqrt(pow(element[0]-centre[0],2) +
                    pow(element[1]-centre[1],2));
        break;
        
    case 3:
        return sqrt(pow(element[0]-centre[0],2) +
                    pow(element[1]-centre[1],2) +
                    pow(element[2]-centre[2],2) +
                    (DIST_FACTOR * pow(row - location.x,2)) +
                    (DIST_FACTOR * pow(col - location.y,2)));
        break;
        
    }
    return -1;
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
            cluster_locations.push_back(cv::Point2i(row,col));
            std::cout << "row: " << row << " col: " << col << std::endl;
            std::cout << image.at<cv::Vec3b>(row,col) << std::endl;
            cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
        }
        break;

    case 2:
        std::cout << "reached case 2" << std::endl;
        for(int row = 0; row < image.rows; row++){
            for(int col = 0; col < image.cols; col++){
                labels.at<uchar>(row,col) = randCluster(generator);
            }
        }       
        
        for(int cluster = 0; cluster < k; cluster++){
            cv::Vec3i sum = cv::Vec3i(0,0,0);
            cv::Point2i loc_sum = cv::Point2i(0,0);
            int count = 0;
            for(int row = 0; row < labels.rows; row++){
                for(int col = 0; col < labels.cols; col++){
                    if(labels.at<uchar>(row,col) == cluster){
                        cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                        /* sum[0] += pixel[0];
                           sum[1] += pixel[1];
                           sum[2] += pixel[2];*/
                        loc_sum.x += row;
                        loc_sum.y += col;
                        sum += pixel;
                        count++;
                    }
                }
            }
            //cv::Vec3b temp = cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count);
            // cv::Point2i loc_temp = cv::Point2i(loc_sum.x/count, loc_sum.y/count);
            //std::cout << temp << std::endl;
            clusters.push_back(cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count));
            cluster_locations.push_back(cv::Point2i(loc_sum.x/count, loc_sum.y/count));
        }
        break;

    case 3:
        //K-means++ step 1
        int initRow = randRow(generator);
        int initCol = randCol(generator);
        clusters.push_back(image.at<cv::Vec3b>(initRow,initCol));
        cluster_locations.push_back(cv::Point2i(initRow,initCol));
        //Repeat until k centres have been chosen
        for(int i = 1; i < k; i++){
            cv::Mat distances = cv::Mat(image.rows, image.cols, CV_64FC1);
            for(int row = 0; row < image.rows; row++){
                for(int col = 0; col < image.cols; col++){
                
                    double min_dist = std::numeric_limits<double>::max();
                    for(int centre = 0; centre < clusters.size(); centre++){
                        double distance = computeDistance(row, col, centre);
                        // std::cout << "distance: " << distance << std::endl;
                        if(distance < min_dist)
                            min_dist = distance;
                        
                    
                    }
                    distances.at<double>(row,col) = pow(min_dist,2);
                }
            }
            
            double weight_sum = 0;
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
                        cluster_locations.push_back(cv::Point2i(row,col));
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

    std::vector<cv::Vec3b> prev_clusters;
    int count = 0;
    bool first_itertion = true;
    
    while(count < k){
        count = 0;
        //std::cout << i << std::endl;
        for(int row = 0; row < image.rows; row++){
            for(int col = 0; col < image.cols; col++){
                //int label = -1;
                double min_dist = std::numeric_limits<double>::max();
                for(int centre = 0; centre < clusters.size(); centre++){
                    cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                    cv::Vec3b cluster = clusters[centre];
                    double distance = computeDistance(row, col, centre);
                
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
                        /*sum[0] += pixel[0];
                          sum[1] += pixel[1];
                          sum[2] += pixel[2];*/
                        sum += pixel;
                        count++;
                    }
                }
            }
            //random cluster can result in clusters that have no assigned elements
            //Likely still a bug here actually.
            //  std::cout << sum << std::endl;
            if(count > 0){
                //std::cout << sum << std::endl;
                // std::cout << "cluster " << centre << "  before: "    \
                //  << clusters[centre] << std::endl;
                clusters[centre] = cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count);
                // std::cout << "cluster " << centre << "  after: " << clusters[centre] \
                // << std::endl;
            }
        }

        if(!first_itertion){
            for(int i = 0; i < clusters.size(); i++){
                if(clusters[i] == prev_clusters[i]) count++;
            }
        } else {
            first_itertion = false;
        }
        
        prev_clusters = clusters;
        std::cout << "stable clusters = " << count << std::endl;

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
                
int main(int argc, char **argv){


    if(argc != 7){
        std::cout << "Usage: ./JLaPine_asgn2 k cluster_init dist_measure dist_factor imageFilePath" << std::endl;
        return -1;
    }
    
    k = atoi(argv[1]);
    distance_method = atoi(argv[3]);
    image = cv::imread(argv[5]);
    labels = cv::Mat(image.rows, image.cols, CV_8UC1);
    if(!image.data){
        std::cout << "Failed to locate image" << std::endl;
        return -1;
    }
    DIST_FACTOR = atof(argv[4]);
    
    if(distance_method == 2)
        cv::cvtColor(image, image, CV_BGR2HSV);
    
    std::cout << image.type() << std::endl;
    initClusters(atoi(argv[2]));

    kMeans();

    if(distance_method == 2)
        cv::cvtColor(image, image, CV_HSV2BGR);
    cv::imshow("",image);
    cv::waitKey(0);
    cv::imwrite(argv[6], image);
    return 0;
}
