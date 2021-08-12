# Face-Detection
Crime analysis and offender detection in Video databaseIntroduction:
 
              The aim of the project is to use Big data frame works like hadoop and spark to analyse and detect offenders movement in a video data base, the output we get is the videofile_name mapped to the offenders names if they are present in the video 

DataSet:
              https://www.di.ens.fr/~laptev/actions/hollywood2/ size:~ 15 GB file names in f2.txt

Modules used:
              face-recognition for matching face encodings with faces found in the video.
                                               opencv-python for detecting faces in the video.
                                               both of the above use numpy.
Setup:
              ->set up contains 8 core cpu and running kali linux
              ->hadoop-3.3.0 binaries downloaded
              ->jdk-15.0.1 binaries downloaded and path exported to this
              -> python3.8 
           ->spark-3.0.1-bin-hadoop3.2 binaries downloaded and environment set to python3.8 and java, which is downloaded.

configuration:

              ->mapped-site.xml
              ->export hadoop-dir-config
              ->export HADOOP_HOME=/home/sreechakra/Desktop/hadoop_install/hadoop-3.3.0
              ->export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
              ->export PYSPARK_DRIVER_PYTHON=/usr/bin/python3.8
              ->export PYSPARK_PYTHON=/usr/bin/python3.8

             
commands used:

1) normal setup to start hadoop running in pseudo distro mode by running miniproject_cs505.py
from desktop
2)bin/hdfs dfs -mkdir /user
3)bin/hdfs dfs -mkdir /user/sree
4)bin/hdfs dfs -mkdir /user/sree/input
5)bin/hdfs dfs -put /home/sreechakra/Desktop/f3.txt /user/sree/input
6)bin/hdfs dfs -put /home/sreechakra/Desktop/f4.txt/user/sree/input
7)bin/hadoop  jar share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -D mapred.map.tasks=2 -input /user/sree/input -output /user/sree/output -mapper facerecognition_streaming_recogfunc_forparallelism.py   -reducer test.py  -file /home/sreechakra/Desktop/hadoop_install/hadoop-3.3.0/facerecognition_streaming_recogfunc_forparallelism.py -file /home/sreechakra/Desktop/hadoop_install/hadoop-3.3.0/test.py


8)bin/spark-submit --master local[4] /home/sreechakra/Desktop/hadoop_install/hadoop-3.3.0/facerecognition_streaming_with_SparkandYarn.py --py-files /home/sreechakra/Desktop/hadoop_install/virtualEnv.zip


Files:

           1)hadoop-3.3.0 binaries
           2)jdk-15.0.1 binaries
           3)spark-3.0.1-bin-hadoop3.2 binaries
           4)hadoop mapreduce 
                        - mapper ->face recognition_streaming_recogfunc_forparallelism.py
                        - reducer ->test.py
           5)spark submit 
                        - facerecognition_streaming_with_sparkandYarn.py
           6)extra files
                        - harcascade_frontalface_defaullt.xml

Codes: https://drive.google.com/file/d/1Ml6ouMvA4JLHAllEH4EAVhS4EpqWCNtY/view?usp=sharing

Motivation:

              The project is motivated to provide a analysis of crimes through offenders detection from video footage where big data is very helpful since to detect ‘M’ offenders accross ’N’ video files
where each frame may contain ‘L’ faces and each video is of ‘O’ duration .The above stats show that in linear programming it would take M*N*(L+k(L))*O units of time , where k(L) is the time taken to detect L faces in the frame, here we can decrease the time linearly with the help of bigdata 
,for example if the N video files is split into 355 input splits then the time would be                    M*(N/355)*(L+k(L))*O reduced to a factor of no of input splits.

Methodology:

               The methodology is to first build a py script which takes as input a video file name and reads through it frame by frame and detect faces with the help of opencv_python , then we will have the offenders face_encodings calculated through face_recognition function and match them with the faces found in the frame, the output is the key=filename ,value = face_names of offenders if any. 
               The second step is to use the hadoop streaming to input files and above py script as mapper , the reducer is similarly built where the output key = videofile_name ,value = list of offenders  in this video_file.
               The third step is to parallelise the above task , since this can’t be done with hadoop streaming in pseudo distributed mode even if the input is split to many more, we use spark and make use of local[4] option to setup a spark context to make the job spread to 4 , each task uses 2 cores in the 8 core laptop,




Result:

               The hadoop streaming works fine with the mapper and reducer py scripts built but
it can not use the resources properly even by changing map.cores.max , map.cores.min to 4 or by explicitly passing them in the terminal command , this is only possible with yarn as mapred.framework but yarn has problems running py scripts ,yarn needs spark to run py scripts, so to use the resources we needed to use spark and tweaked the mapper we built for hadoop streaming , this works fine and following is the result when input split is 2.
input split is 2:
2 jobs are running in parallel:

these are the final results for input file f4.txt:








Discussion:

                 We can improve it further to cluster mode which only needs python3.8 env or its virtualenv to be exported as .zip through spark-submit.we can also implement a parallel model for streaming.


Conclusion:

                The code works fine in pseudo distributed mode , spark has extra functionality to set the no of threads for each task and the no of cores each task uses, my code uses 4 cores that is 2 threads per task.
