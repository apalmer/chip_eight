using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Playground.Domain;

namespace Playground.Models
{
    public class EmployeeSearchResultsModel
    {
        public Playground.BusinessLogic.EmployeeSearchCriteria Criteria { get; set; } 
        public List<Employee> SearchResults { get; set; }
    }
}