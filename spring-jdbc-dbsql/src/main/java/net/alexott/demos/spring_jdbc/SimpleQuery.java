package net.alexott.demos.spring_jdbc;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import com.databricks.client.jdbc.Driver;

import java.util.List;
import java.util.Map;

public class SimpleQuery {
    public static void main(String[] args) {
        // Variables to update
        String host = "";
        String httpPath = "";
        String token = "";
        String query = "select * from default.table";

        String jdbcUrl = "jdbc:databricks://" + host + ":443/default;transportMode=http;ssl=1;httpPath=" +
                httpPath + ";AuthMech=3;UID=token;PWD=" + token;

        // define data source
        SimpleDriverDataSource ds = new SimpleDriverDataSource();
        ds.setDriver(new Driver());
        ds.setUrl(jdbcUrl);
        JdbcTemplate jdbcTemplate = new JdbcTemplate(ds);

        // query data
        List<Map<String, Object>> data = jdbcTemplate.queryForList(query);
        int cnt = 0;
        for (Map<String, Object> row: data) {
            System.out.format("Row(%5d)[", cnt+1);
            int i=0;
            for (Map.Entry<String, Object> entry: row.entrySet()) {
                if (i > 0) {
                    System.out.print(", ");
                }
                System.out.print(entry.getKey()+"='" + entry.getValue() + "'");
                i++;
            }
            System.out.println("]");
            cnt++;
        }
        System.out.format("There are %d rows in the table\n", cnt);
    }
}
