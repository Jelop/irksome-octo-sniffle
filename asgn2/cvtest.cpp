#include <opencv2/opencv.hpp>
#include <iostream>
#include <limits>
#include <random>

int k;
cv::Mat image;
std::vector<cv::Vec3b> clusters;
cv::Mat labels;

void initClusters(int type){

    std::default_random_engine generator;
    std::uniform_int_distribution<int> randRow(0,image.rows-1);
    std::uniform_int_distribution<int> randCol(0,image.cols-1);

    
    switch(type){

    case 1:
        for(int i = 0; i < k; i++){
            int row = randRow(generator);
            int col = randCol(generator);
            clusters.push_back(image.at<cv::Vec3b>(row,col));
            std::cout << "row: " << row << " col: " << col << std::endl;
            std::cout << image.at<cv::Vec3b>(row,col) << std::endl;
        }
        break;
    }
    
}

void kMeans(){

    for(int i = 0; i < 20; i++){
        std::cout << i << std::endl;
        for(int row = 0; row < image.rows; row++){
            for(int col = 0; col < image.cols; col++){
                int label = -1;
                double min_dist = std::numeric_limits<double>::max();
                for(int centre = 0; centre < clusters.size(); centre++){
                    cv::Vec3b pixel = image.at<cv::Vec3b>(row,col);
                    cv::Vec3b cluster = clusters[centre];
                    double distance = sqrt(pow(pixel[0]-cluster[0],2) +
                                           pow(pixel[1]-cluster[1],2) +
                                           pow(pixel[2]-cluster[2],2));
                    if(distance < min_dist){
                        labels.at<uchar>(row,col) = centre;
                        min_dist = distance;
                    }
                }
            }
        }

        for(int centre = 0; centre < clusters.size(); centre++){
            cv::Vec3i sum = cv::Vec3i(0,0,0);
            int count;
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
            clusters[centre] = cv::Vec3b(sum[0]/count,sum[1]/count,sum[2]/count);
        }

    

    for(int centre = 0; centre < clusters.size(); centre++){
        for(int row = 0; row < labels.rows; row++){
            for(int col = 0; col < labels.cols; col++){
                if(labels.at<uchar>(row,col) == centre){
                    image.at<cv::Vec3b>(row,col)[0] = clusters[centre][0];
                    image.at<cv::Vec3b>(row,col)[1] = clusters[centre][1];
                    image.at<cv::Vec3b>(row,col)[1] = clusters[centre][2];
                }
            }
        }
    }
    }
}
                
int main(int argc, char **argv){


    if(argc != 3){
        std::cout << "Usage: ./kMeans k  imageFilePath" << std::endl;
        return -1;
    }

    k = atoi(argv[1]);
    image = cv::imread(argv[2]);
    labels = cv::Mat(image.rows, image.cols, CV_8UC1);
    if(!image.data){
        std::cout << "Failed to locate image" << std::endl;
        return -1;
    }
    std::cout << image.type() << std::endl;
    initClusters(1);

    kMeans();
    cv::imshow("",image);
    cv::waitKey(0);
    return 0;
}
