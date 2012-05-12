using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Playground.Domain;

namespace Playground.BusinessLogic
{
    public class EmployeeSearch
    {
        public List<Employee> Search(EmployeeSearchCriteria criteria)
        {
            var searchResults = Playground.DataAccess.ADOdotNET.EmployeeSearch.Search(
                criteria.FirstName,
                criteria.LastName,
                criteria.Organization,
                criteria.JobTitle,
                criteria.Address,
                criteria.City,
                criteria.State,
                criteria.ZipCode,
                criteria.MaximumRecords,
                criteria.SortByColumn,
                criteria.SortAscending,
                criteria.GroupByColumn,
                criteria.GroupBySortAscending,
                criteria.RecordsPerPage,
                criteria.PageNumber
            );
            return searchResults;
        }
    }
}
