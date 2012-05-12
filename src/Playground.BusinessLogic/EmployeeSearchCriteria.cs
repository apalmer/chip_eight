using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Playground.BusinessLogic
{
    public class EmployeeSearchCriteria
    {
        public Int32 ID { get; set; }
        public String FirstName { get; set; }
        public String LastName { get; set; }
        public String Organization { get; set; }
        public String JobTitle { get; set; }
        public String Address { get; set; }
        public String City { get; set; }
        public String State { get; set; }
        public String ZipCode { get; set; }
        public int? MaximumRecords { get; set; }
        public String SortByColumn { get; set; }
        public Boolean? SortAscending { get; set; }
        public String GroupByColumn { get; set; }
        public Boolean? GroupBySortAscending { get; set; }
        public Int32? RecordsPerPage { get; set; }
        public Int32? PageNumber { get; set; }

        public List<String> ValidationErrors { get; private set; }

        public Boolean Validate()
        {
            return true;
        }
    }
}
