import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class EmailLogAnalysis {

    // Mapper class that processes each line of the input file
    public static class EmailMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text recipient = new Text();
        // Regular expression to extract the recipient email address
        private Pattern pattern = Pattern.compile("to=<(.+?)>");

        // The map method processes each line of the input file
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            Matcher matcher = pattern.matcher(value.toString());
            if (matcher.find()) {
                // Set the recipient email address as the key
                recipient.set(matcher.group(1));
                // Write the key-value pair to the context
                context.write(recipient, one);
            }
        }
    }

    // Reducer class that aggregates the counts of emails for each recipient
    public static class EmailReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        // The reduce method processes each group of values associated with a key
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            // Sum up the counts for each recipient
            for (IntWritable val : values) {
                sum += val.get();
            }
            // Set the result and write the key-value pair to the context
            result.set(sum);
            context.write(key, result);
        }
    }

    // Main method to configure and run the MapReduce job
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        // Create a new job instance
        Job job = Job.getInstance(conf, "email log analysis");
        // Set the jar file that contains the driver, mapper, and reducer classes
        job.setJarByClass(EmailLogAnalysis.class);
        // Set the mapper class
        job.setMapperClass(EmailMapper.class);
        // Set the combiner class, which is executed after the mapper but before the reducer
        job.setCombinerClass(EmailReducer.class);
        // Set the reducer class
        job.setReducerClass(EmailReducer.class);
        // Set the output key and value types for the job
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        // Set the input and output paths for the job
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        // Exit the program based on the job result
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

