using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Playground.BusinessLogic;

namespace Playground.Models
{
    public class EmployeeSearchModel
    {
        public List<String> ValidationMessages { get; set; }
        public Playground.BusinessLogic.EmployeeSearchCriteria Criteria { get; set; }

        public EmployeeSearchModel()
        {
            ValidationMessages = new List<String>();
            Criteria = new EmployeeSearchCriteria();
        }
    }
}