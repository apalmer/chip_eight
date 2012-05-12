using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using Playground.Domain;

namespace Playground.DataAccess.ADOdotNET
{
    public class EmployeeSearch
    {
        public static List<Playground.Domain.Employee> Search(String firstName, String lastName, String organization, String jobTitle, String address, String city, String state, String zipCode, Int32? maximumRecords, String sortByColumn, Boolean? sortByAscending, String groupByColumn, Boolean? groupBySortAscending, Int32? recordsPerPage, Int32? pageNumber)
        {
            List<Playground.Domain.Employee> results = new List<Playground.Domain.Employee>();
            var connectionString = System.Configuration.ConfigurationManager.ConnectionStrings["Playground"].ToString();
            using (var connection = new System.Data.SqlClient.SqlConnection(connectionString))
            {
                connection.Open();
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "Employee_Search";
                    command.CommandType = CommandType.StoredProcedure;
                    command.Parameters.Add(new SqlParameter("@FirstName", SqlDbType.NVarChar){Direction = ParameterDirection.Input, Value = firstName});
                    command.Parameters.Add(new SqlParameter("@LastName", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = lastName });
                    command.Parameters.Add(new SqlParameter("@Organization", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = organization });
                    command.Parameters.Add(new SqlParameter("@JobTitle", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = jobTitle });
                    command.Parameters.Add(new SqlParameter("@Address", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = address });
                    command.Parameters.Add(new SqlParameter("@City", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = city });
                    command.Parameters.Add(new SqlParameter("@State", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = state });
                    command.Parameters.Add(new SqlParameter("@ZipCode", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = zipCode });
                    command.Parameters.Add(new SqlParameter("@MaximumRecords", SqlDbType.Int) { Direction = ParameterDirection.Input, Value = maximumRecords });
                    command.Parameters.Add(new SqlParameter("@SortByColumn", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = sortByColumn });
                    command.Parameters.Add(new SqlParameter("@SortAscending", SqlDbType.Bit) { Direction = ParameterDirection.Input, Value = sortByAscending });
                    command.Parameters.Add(new SqlParameter("@GroupByColumn", SqlDbType.NVarChar) { Direction = ParameterDirection.Input, Value = groupByColumn });
                    command.Parameters.Add(new SqlParameter("@GroupBySortAscending", SqlDbType.Bit) { Direction = ParameterDirection.Input, Value = groupBySortAscending });
                    command.Parameters.Add(new SqlParameter("@RecordsPerPage", SqlDbType.Int) { Direction = ParameterDirection.Input, Value = recordsPerPage });
                    command.Parameters.Add(new SqlParameter("@PageNumber", SqlDbType.Int) { Direction = ParameterDirection.Input, Value = pageNumber });

                    using(System.Data.IDataReader reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            Playground.Domain.Employee result = new Playground.Domain.Employee();
                            result.ID = reader.GetInt32(0);
                            result.FirstName = reader.GetString(1);
                            result.LastName = reader.GetString(2);
                            result.Organization = reader.GetString(3);
                            result.JobTitle = reader.GetString(4);
                            result.Address = reader.GetString(5);
                            result.City = reader.GetString(6);
                            result.State = reader.GetString(7);
                            result.ZipCode = reader.GetString(8);

                            results.Add(result);
                        }
                    }
                }
                connection.Close();
            }
            return results;
        }
    }
}
